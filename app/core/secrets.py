"""Auth hash parameters"""
HASH_NAME = 'sha256'
PASS_ENCODE = 'utf-8'
SALT = b'\x0eE\x1f\x7f\x92\xe3\x19\xbdzz\xae"\x19\xca\x07E'
ITERATIONS = 1000

"""Encryption data."""
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_SEC = 10
SECRET_KEY = b'some_secret_key_here'
