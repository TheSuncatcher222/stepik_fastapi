from datetime import datetime
from typing import Annotated

from fastapi import (
    FastAPI, HTTPException, Response, status, Request,
    Cookie, Depends, Header)
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from auth.auth import (
    decode, password_hash, user_token_generate,
    SECRET_TOKEN_ENCODE)
from core.core import PRODUCTS, USERS, USERS_USERNAMES
from db_fake import DB_FAKE_INIT
from models.models import (
    PRODUCT_CATEGORIES_LIST,
    ProductModel, UsersAuthModel, UserModel, UserRegisterModel,
    UserWithoutPasswordModel)

app: FastAPI = FastAPI(title='My first FastAPI app')
security: HTTPBasic = HTTPBasic()

db: dict[str, dict[int, any]] = DB_FAKE_INIT


@app.get('/')
async def index(response: Response, last_visit=Cookie()):
    with open(file='app/index.html',
              mode='r',
              encoding='utf-8') as html_file:
        html_content = html_file.read()
    return HTMLResponse(content=html_content, status_code=status.HTTP_200_OK)


@app.post('/cookie/read/')
async def index_cookie_read(last_visit=Cookie()):
    return {"last visit": last_visit}


@app.post('/cookie/set/')
async def index_cookie_set(response: Response):
    now = datetime.now()
    response.set_cookie(key="last_visit", value=now)
    return {"message": "Cookies set!"}


@app.get('/download/')
async def download_requirements():
    return FileResponse(
        path='requirements.txt',
        filename='Project_Requirements.txt',
        status_code=status.HTTP_200_OK,
        media_type='text/txt')


@app.get('/header-read/')
async def header_read(
        accept_language: Annotated[list[str] | None, Header()] = None,
        authorization: Annotated[str | None, Header()] = None,
        user_agent: Annotated[list[str] | None, Header()] = None):
    required_headers: dict[str, str | list[str]] = {
        'Accept-Language': accept_language,
        'Authorization': authorization,
        'User-Agent': user_agent}
    missing_headers: list[str] = [
        header for header, value in required_headers.items() if value is None]
    if missing_headers:
        return JSONResponse(
            content={'Missed Headers': missing_headers},
            status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse(
        content=required_headers,
        status_code=status.HTTP_200_OK)


@app.get('/products/', response_model=list[ProductModel])
async def products_get(limit: int = 3, offset: int = 0):
    return list(db[PRODUCTS].values())[offset:limit+offset]


@app.get('/products/search/', response_model=list[ProductModel])
async def products_get_search(
        keyword: str,
        category: str = None,
        limit: int = 10):
    if category and category not in PRODUCT_CATEGORIES_LIST:
        raise HTTPException(status_code=401, detail="Category doesn't exist!")
    response: list[ProductModel] = list(
        filter(lambda product: keyword.lower() in product.name.lower(),
               db[PRODUCTS].values()))
    if category:
        response: list[ProductModel] = list(
            filter(lambda product: category.lower() == product.category,
                   response))
    return response[:limit]


@app.get('/products/{id}/', response_model=ProductModel | dict)
async def products_get_id(id: int):
    product = db[PRODUCTS].get(id)
    if product is None:
        raise HTTPException(status_code=404, detail="Not Found!")
    return product


@app.post('/products/', response_model=ProductModel)
async def products_post(product: ProductModel):
    new_id: int = len(db[PRODUCTS]) + 1
    posted_product: ProductModel = ProductModel(
        id=new_id,
        name=product.name,
        category=product.category,
        price=product.price)
    db[PRODUCTS][new_id] = posted_product
    return posted_product


@app.get('/users/', response_model=list[UserWithoutPasswordModel])
async def users_get(limit: int = 3, offset: int = 0):
    return list(db[USERS].values())[offset:limit+offset]


@app.post('/users/', response_model=UserWithoutPasswordModel)
async def users_post(user: UserRegisterModel):
    if user.username in db[USERS_USERNAMES]:
        raise HTTPException(
            status_code=401, detail="User with that username exists!")
    new_id: int = len(db[USERS]) + 1
    posted_user = UserModel(
        id=new_id,
        username=user.username,
        password=user.password,
        age=user.age)
    db[USERS][new_id] = posted_user
    db[USERS_USERNAMES].append(user.username)
    return posted_user


@app.get('/users/me/', response_model=UserWithoutPasswordModel)
async def users_me_get(session_token=Cookie()):
    username, token = session_token.split(".")
    username = decode(encrypted_data=username)
    if (token != SECRET_TOKEN_ENCODE or username not in db[USERS_USERNAMES]):
        raise HTTPException(status_code=401, detail="Permission denied!")
    return [user for user in db[USERS].values()
            if username == user.username][0]


def authenticate_user(auth_data: HTTPBasicCredentials | UsersAuthModel):
    for user in db[USERS].values():
        if (auth_data.username == user.username and
                user.password == password_hash(
                    password=auth_data.password)):
            return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials")


def authenticate_credentials(
        credentials: HTTPBasicCredentials = Depends(security)):
    return authenticate_user(auth_data=credentials)


def authenticate_body(login_data: UsersAuthModel):
    return authenticate_user(auth_data=login_data)


@app.get('/users/me_protected/', response_class=dict[str, str])
async def users_me_protected_get(user=Depends(authenticate_credentials)):
    return JSONResponse(
        content={
            "message": ("You have access to the protected resource, "
                        f"{user.username}!")},
        status_code=status.HTTP_200_OK)


@app.post('/users/login/', response_model=dict[str, str])
async def users_login(user=Depends(authenticate_body)):
    response = JSONResponse(
            content={"Confirm": "Welcome!"},
            status_code=status.HTTP_200_OK)
    response.set_cookie(
        key='session_token',
        value=user_token_generate(username=user.username))
    return response


@app.get('/users/{id}/', response_model=UserWithoutPasswordModel | dict)
async def users_get_id(id: int):
    return db[USERS].get(id, JSONResponse(
        content={"Bad Request": "User doesn't exist!"},
        status_code=status.HTTP_404_NOT_FOUND))


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail})


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
