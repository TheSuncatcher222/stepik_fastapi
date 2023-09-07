from base64 import urlsafe_b64encode, urlsafe_b64decode
import hashlib

from fastapi import HTTPException, status
import jwt


from core.secrets import (
    HASH_NAME, JWT_ALGORITHM, PASS_ENCODE, SALT, ITERATIONS, SECRET_KEY)


def encode(data: str) -> str:
    encrypted_bytes: bytes = bytes(data, PASS_ENCODE) + SECRET_KEY
    encrypted_data: bytes = urlsafe_b64encode(encrypted_bytes)
    return encrypted_data.decode(PASS_ENCODE)


def decode(encrypted_data: str) -> str:
    encrypted_bytes: bytes = urlsafe_b64decode(encrypted_data)
    decrypted_data: str = (
        encrypted_bytes[:-len(SECRET_KEY)].decode(PASS_ENCODE))
    return decrypted_data


def jwt_token_create(data: dict):
    """Encode dict data to jwt token."""
    return jwt.encode(payload=data, key=SECRET_KEY, algorithm=JWT_ALGORITHM)


def jwt_token_read(data: dict):
    """Decode dict data from jwt token."""
    try:
        return jwt.decode(jwt=data, key=SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        detail = "Token has expired!"
    except jwt.InvalidTokenError:
        detail = "Token is broken!"
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail)


def password_hash(password: str) -> str:
    """Hash user password to write in db."""
    return hashlib.pbkdf2_hmac(
        hash_name=HASH_NAME,
        password=password.encode(PASS_ENCODE),
        salt=SALT,
        iterations=ITERATIONS)
