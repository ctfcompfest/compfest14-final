import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'db3485d0f1bc54303cdaf9dabb1d78d961e50b233efeec9e663aea5df89490f5.db')
ENCRYPTION_KEY = 'T0t4llyS3cureP4s5word'

class AppConfig(object):
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    SECRET_KEY = os.urandom(32)