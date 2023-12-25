"""
Главный модуль FastAPI сервиса.

Осуществляет запуск проекта, подключение базы данных, регистрацию эндпоинтов.
"""

import os
import sys

from fastapi import FastAPI
import uvicorn

# INFO: добавляет корневую директорию проекта в sys.path для возможности
#       использования абсолютных путей импорта данных из модулей.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.config import ASGI_PORT, DEBUG, WORKERS_AMOUNT
from src.database import (
    db,
    connect_to_database, disconnect_from_database,
    TBL_NAME_USER,
)
from src.logger import get_logger

from src.auth.routers import router as router_auth
from src.auth.schemas import (
    USER_EMAIL_MAX_LEN, USER_HASH_PASS_LEN,
)

app: FastAPI = FastAPI(
    debug=DEBUG,
    title='Tradings FastAPI',
    description='My test FastAPI project',
    version='0.0.1',
)

logger = get_logger(name=__name__)


# TODO: использовать lifespan.
@app.on_event('startup')
async def startapp_db_client():
    logger.debug('Setup connection to db')
    await connect_to_database()
    logger.info('Setup connection to db is succeed')
    query: str = (
        f'DROP TABLE IF EXISTS {TBL_NAME_USER}'
    )
    await db.execute(query=query)
    query: str = (
        f'CREATE TABLE IF NOT EXISTS {TBL_NAME_USER} ('
        f'      id SERIAL PRIMARY KEY,'
        f'      password VARCHAR({USER_HASH_PASS_LEN}) NOT NULL,'
        f'      email VARCHAR({USER_EMAIL_MAX_LEN}) NOT NULL UNIQUE'
        f'  )'
        f';'
    )
    await db.execute(query=query)


# TODO: использовать lifespan.
@app.on_event('shutdown')
async def shutdown_db_client():
    logger.debug('Close connection to db')
    await disconnect_from_database()
    logger.info('Close connection to db is succeed')


app.include_router(
    router=router_auth,
    prefix='/auth',
    tags=['auth'],
)


if __name__ == '__main__':
    """Автозапуск ASGI и сервиса."""
    uvicorn.run(
        app='main:app',
        host='127.0.0.1',
        port=ASGI_PORT,
        reload=True,
        workers=WORKERS_AMOUNT,
    )
