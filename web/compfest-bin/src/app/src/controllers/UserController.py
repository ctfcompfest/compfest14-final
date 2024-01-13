from functools import wraps

from ..models.User import FULLNAME_MAX_LENGTH
from ..models.User import User
from ..models import db


def return_on_failure(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return

    return wrapped


class UserManager(object):
    @staticmethod
    def update_profile(user, fullname):
        if len(fullname) > FULLNAME_MAX_LENGTH:
            raise Exception('Fullname length should not exceeds 100 character')

        try:
            with db.engine.connect() as connection:
                query = f"""UPDATE users set fullname="{str(fullname)}" WHERE id='{user.id}'"""
                result = connection.execute(query)
        except:
            raise Exception('Unexpected error occured')

    @staticmethod
    def get_user_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.filter_by(id=user_id).first()

    @staticmethod
    def is_eligible(username, user_id):
        user = User.query.filter_by(
            id=user_id,
            username=username
        ).first()

        if user:
            return True
            
        return False


class UserLoginManager(object):
    def __init__(self, body):
        self.username = body.get('username')
        self.password = body.get('password')
        
        self.user = UserManager.get_user_by_username(self.username)

    @return_on_failure
    def is_user_authorized(self):
        return self.user.verify_password(self.password)


class UserRegisterManager(object):
    def __init__(self, body):
        self.username = body.get('username')
        self.password = body.get('password')

        if self.username and self.password:
            self.user = User(self.username, self.password)
        else:
            raise Exception('Username/Password should not be empty')
    
    def is_user_existed(self):
        return self.user.verify_uniqueness()

    def add_user(self):
        db.session.add(self.user)
        db.session.commit()
