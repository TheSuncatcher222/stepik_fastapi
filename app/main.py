"""
=================
My first FastAPI project! Study new framework.
=================
Project tech data:
    - custom JWT authentication
    - to be more...
=================
Author: Svidunovich Kirill
        TheSuncatcher222@gmail.com
        https://github.com/TheSuncatcher222
=================
Project description and instructions:
https://github.com/TheSuncatcher222/stepik_fastapi
=================
"""

from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException, status, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from auth.auth import password_hash, jwt_token_create, jwt_token_read
from core.core import HTTPEXCEPTION_401, STRTIME_FORMAT, USERS, USERS_USERNAMES
from core.secrets import JWT_EXPIRATION_SEC
from db_fake import DB_FAKE_INIT
from models.models import (
    UsersAuthModel, UserModel, UserRegisterModel, UserRoles,
    UserWithoutPasswordModel)

app: FastAPI = FastAPI(title='My first FastAPI app')
# TODO: разобраться с tokenUrl
oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl='login')

db: dict[str, dict[int, any]] = DB_FAKE_INIT


def authenticate_user(auth_data: UsersAuthModel):
    """Authenticate user with given auth_data: username, password."""
    for user in db[USERS].values():
        if (auth_data.username == user.username and
                user.password == password_hash(
                    password=auth_data.password)):
            return user
    raise HTTPEXCEPTION_401


def authenticate_body(login_data: UsersAuthModel):
    """Get username and password data from the body of the request
    and send to authenticate_user."""
    return authenticate_user(auth_data=login_data)


def get_user_from_jwt(jwt: str) -> dict | None:
    """Read JWT token and return user if valid."""
    jwt_token: dict = jwt_token_read(data=jwt)
    id, expired = jwt_token.get('id'), jwt_token.get('expired')
    if (expired is None or
            datetime.strptime(expired, STRTIME_FORMAT) < datetime.utcnow() or
            id is None):
        return None
    return db[USERS].get(id)


@app.get('/users/', response_model=list[UserWithoutPasswordModel])
async def users_get(limit: int = 3, offset: int = 0):
    """Return list of users with limit and offset without pagination."""
    return list(db[USERS].values())[offset:limit+offset]


@app.post('/users/', response_model=UserWithoutPasswordModel)
async def users_post(user: UserRegisterModel):
    """Register new user."""
    if user.username in db[USERS_USERNAMES]:
        raise HTTPException(
            status_code=400,
            detail="User with that username exists!")
    new_id: int = len(db[USERS]) + 1
    posted_user: UserModel = UserModel(
        id=new_id,
        username=user.username,
        password=user.password,
        age=user.age)
    db[USERS][new_id] = posted_user
    db[USERS_USERNAMES].append(user.username)
    return posted_user


# TODO: read https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
@app.get('/users/me/', response_model=UserWithoutPasswordModel)
async def users_me_get(authorization: str = Depends(oauth2_scheme)):
    """Get JWT and return user data if valid."""
    if not authorization:
        raise HTTPEXCEPTION_401
    user: dict = get_user_from_jwt(jwt=authorization)
    if user is None:
        raise HTTPEXCEPTION_401
    return user


@app.post('/login/')
async def users_login(user=Depends(authenticate_body)):
    """Authenticate user and set user token to the cookies."""
    exp = (datetime.utcnow() + timedelta(seconds=JWT_EXPIRATION_SEC)
           ).strftime(STRTIME_FORMAT)
    jwt_token: str = jwt_token_create(
        data={
            "expired": exp,
            "id": user.id,
            "username": user.username,
            "age": user.age})
    response = JSONResponse(
            content={"jwt_token": f'Bearer {jwt_token}'},
            status_code=status.HTTP_200_OK)
    return response


@app.post('/users/get_my_role/')
async def users_get_my_role(authorization: str = Depends(oauth2_scheme)):
    """Get JWT and return user role."""
    user: dict = get_user_from_jwt(jwt=authorization)
    if user is None:
        role: str = UserRoles.is_anonymous
    else:
        role: str = user.role
    return JSONResponse(
        content={"Current role": role},
        status_code=status.HTTP_200_OK)


@app.get('/users/{id}/', response_model=UserWithoutPasswordModel)
async def users_get_id(id: int):
    user: dict = db[USERS].get(id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User doesn't exist!")
    return user


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Catch HTTPExceptions from app and return it to the client."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=exc.headers)


if __name__ == '__main__':
    """Semi-start of the app."""
    import uvicorn
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
