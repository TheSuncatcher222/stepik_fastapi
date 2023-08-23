import hashlib

HASH_NAME = 'sha256'
PASS_ENCODE = 'utf-8'
SALT = b'\x0eE\x1f\x7f\x92\xe3\x19\xbdzz\xae"\x19\xca\x07E'
ITERATIONS = 1000


def hash_password(password: str) -> str:
    return hashlib.pbkdf2_hmac(
        hash_name=HASH_NAME,
        password=password.encode(PASS_ENCODE),
        salt=SALT,
        iterations=ITERATIONS)
