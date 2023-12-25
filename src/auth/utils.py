"""
Модуль хеширования текстовой строки.
"""

import hashlib

from src.config import HASH_NAME, PASS_ENCODE, SALT, ITERATIONS


def hash_password(raw_password: str) -> str:
    """Создает хэш пароля для сохранения в базе данных."""
    return str(
        hashlib.pbkdf2_hmac(
            hash_name=HASH_NAME,
            password=raw_password.encode(PASS_ENCODE),
            salt=SALT,
            iterations=ITERATIONS,
        )
    )
