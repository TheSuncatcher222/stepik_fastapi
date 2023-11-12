from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.secrets import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

SQLITE_URL: str = 'sqlite://sql_app.db'
POSTGRESQL_URL: str = (
    f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

engine = create_engine(url=SQLITE_URL)

session = sessionmaker(autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass
