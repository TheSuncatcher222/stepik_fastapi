"""
Модуль соединения с базой данных.
"""

from databases import Database

from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

db: Database = Database(url=DATABASE_URL)


"""Управление соединением в базой данных."""


async def connect_to_database():
    """Осуществляет соединение с базой данных."""
    await db.connect()


async def disconnect_from_database():
    """Осуществляет отключение от базы данных."""
    await db.disconnect()


"""Названия таблиц в базе данных."""


TBL_NAME_USER: str = 'user_table'
