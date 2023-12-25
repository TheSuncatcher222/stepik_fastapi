"""
Модуль логики работы эндпоинтов в модуле "auth".
"""

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.database import db, TBL_NAME_USER

from src.auth.schemas import UserRegister
from src.auth.utils import hash_password

router: APIRouter = APIRouter()


@router.post(path='/signup')
async def user_signup(user_data: UserRegister) -> JSONResponse:
    """Осуществляет регистрацию пользователя на сайте."""
    print(user_data.email)
    query: str = (
        'SELECT email '
        f'FROM {TBL_NAME_USER} '
        'WHERE email = :email'
        ';'
    )
    values: dict[str, any] = {
        'email': user_data.email,
    }
    result = await db.execute(query=query, values=values)
    if result is not None:
        return JSONResponse(
            content={'email': 'Этот адрес электронной почты уже зарегистрирован.'},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    query: str = (
        f'INSERT INTO {TBL_NAME_USER} (email, password)'
        'VALUES (:email, :password)'
        ';'
    )
    values: dict[str, any] = {
        'email': user_data.email,
        'password': hash_password(raw_password=user_data.password),
    }
    await db.execute(query=query, values=values)
    return JSONResponse(
        content={'message': 'Signup succeed'},
        status_code=status.HTTP_201_CREATED,
    )


@router.get(path='/users')
async def user_get_list() -> JSONResponse:
    """Возвращает список пользователей."""
    pass
