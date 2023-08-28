from base64 import urlsafe_b64encode, urlsafe_b64decode
import hashlib

from core.secrets import (
    HASH_NAME, PASS_ENCODE, SALT, ITERATIONS,
    SECRET_KEY, SECRET_TOKEN)


def password_hash(password: str) -> str:
    return hashlib.pbkdf2_hmac(
        hash_name=HASH_NAME,
        password=password.encode(PASS_ENCODE),
        salt=SALT,
        iterations=ITERATIONS)


def encode(data: str) -> str:
    encrypted_bytes: bytes = bytes(data, PASS_ENCODE) + SECRET_KEY
    encrypted_data: bytes = urlsafe_b64encode(encrypted_bytes)
    return encrypted_data.decode(PASS_ENCODE)


def decode(encrypted_data: str) -> str:
    encrypted_bytes: bytes = urlsafe_b64decode(encrypted_data)
    decrypted_data: str = (
        encrypted_bytes[:-len(SECRET_KEY)].decode(PASS_ENCODE))
    return decrypted_data


SECRET_TOKEN_ENCODE: bytes = encode(data=SECRET_TOKEN)


def user_token_generate(username: str) -> str:
    encode_username: bytes = encode(data=username)
    return f'{encode_username}.{SECRET_TOKEN_ENCODE}'
