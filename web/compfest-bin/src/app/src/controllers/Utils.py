from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES

from ..config import ENCRYPTION_KEY

import calendar
import base64
import random
import time
import json

def get_current_timestamp():
    gmt = time.gmtime()

    return calendar.timegm(gmt)

def get_random_bytes(size=16):
    return bytearray(random.getrandbits(8) for _ in range(size))

def encrypt(text, session_key):
    now = get_current_timestamp()
    random.seed(now)

    salt = get_random_bytes()
    k1 = PBKDF2(ENCRYPTION_KEY, salt)
    k2 = json.dumps(dict(list(session_key.items())[1:]))

    cipher = AES.new(k1, AES.MODE_GCM)
    cipher.update(base64.b64encode(k2.encode()))

    ciphertext, tag = cipher.encrypt_and_digest(text.encode())
    nonce = cipher.nonce

    return base64.b64encode(
        ciphertext + tag + nonce
    ).decode()

def decrypt(text, session_key, datetime):
    random.seed(int(datetime.timestamp()))

    salt = get_random_bytes()
    k1 = PBKDF2(ENCRYPTION_KEY, salt)
    k2 = json.dumps(dict(list(session_key.items())[1:]))

    text = base64.b64decode(text)

    nonce = text[-16:]
    tag = text[-32:-16]
    ciphertext = text[:-32]

    cipher = AES.new(k1, AES.MODE_GCM, nonce)
    cipher.update(base64.b64encode(k2.encode()))

    return cipher.decrypt_and_verify(ciphertext, tag).decode()
