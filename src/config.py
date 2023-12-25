"""
Модуль с настройками сервиса.
"""

import os

from dotenv import load_dotenv

load_dotenv()


"""Настройки ASGI."""


ASGI_PORT: int = int(os.getenv('ASGI_PORT'))


"""Настройки базы данных."""


DB_HOST: str = os.getenv('DB_HOST')

DB_NAME: str = os.getenv('POSTGRES_DB')

DB_PASS: str = os.getenv('POSTGRES_PASSWORD')

DB_PORT: str = os.getenv('DB_PORT')

DB_USER: str = os.getenv('POSTGRES_USER')


"""Настройки безопасности."""


HASH_NAME: str = os.getenv('HASH_NAME')

PASS_ENCODE: str = os.getenv('PASS_ENCODE')

SALT: bytes = os.getenv('SALT').encode(PASS_ENCODE)

ITERATIONS: int = int(os.getenv('ITERATIONS'))


"""Настройки сервиса."""


DEBUG: str = os.getenv('DEBUG')
if DEBUG == 'True':
    DEBUG: bool = True
else:
    DEBUG: bool = False

if DEBUG:
    WORKERS_AMOUNT: int = 1
else:
    WORKERS_AMOUNT: int = int(os.getenv('WORKERS_AMOUNT'))
