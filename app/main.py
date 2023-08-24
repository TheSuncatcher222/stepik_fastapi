from datetime import datetime

from fastapi import FastAPI, Response, status, Cookie
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse

from auth.auth import hash_password
from core.core import PRODUCTS, USERS, USERS_USERNAMES
from db_fake import DB_FAKE_INIT
from models.models import (
    PRODUCT_CATEGORIES_LIST,
    ProductModel, UsersAuthModel, UserModel, UserRegisterModel,
    UserWithoutPasswordModel)

app: FastAPI = FastAPI(title='My first FastAPI app')

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


@app.get('/products/', response_model=list[ProductModel])
async def products_get(limit: int = 3, offset: int = 0):
    return list(db[PRODUCTS].values())[offset:limit+offset]


@app.get('/products/search/', response_model=list[ProductModel] | dict)
async def products_get_search(
        keyword: str,
        category: str = None,
        limit: int = 10):
    if category and category not in PRODUCT_CATEGORIES_LIST:
        return {"BadRequest": "Category doesn't exist!"}
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
    return db[PRODUCTS].get(id, JSONResponse(
        content={"Bad Request": "Product doesn't exist!"},
        status_code=status.HTTP_404_NOT_FOUND))


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


@app.post('/users/', response_model=UserWithoutPasswordModel | dict)
async def users_post(user: UserRegisterModel):
    if user.username in db[USERS_USERNAMES]:
        return JSONResponse(
            content={"Bad Request": "User with that username exists!"},
            status_code=status.HTTP_400_BAD_REQUEST) 
    new_id: int = len(db[USERS]) + 1
    posted_user = UserModel(
        id=new_id,
        username=user.username,
        password=user.password,
        age=user.age)
    db[USERS][new_id] = posted_user
    db[USERS_USERNAMES].append(user.username)
    return posted_user


@app.get('/users/{id}/', response_model=UserWithoutPasswordModel | dict)
async def users_get_id(id: int):
    return db[USERS].get(id, JSONResponse(
        content={"Bad Request": "User doesn't exist!"},
        status_code=status.HTTP_404_NOT_FOUND))


@app.post('/users/login/', response_model=dict[str, str])
async def users_login(login_data: UsersAuthModel, response=JSONResponse):
    current_user: UsersAuthModel | None = None
    for user in db[USERS].values():
        if login_data.username == user.username:
            current_user: UserModel = user
            break
    if (current_user is None or
            current_user.password != hash_password(
                password=login_data.password)):
        return JSONResponse(
            content={"Bad Request": "Incorrect username or password!"},
            status_code=status.HTTP_400_BAD_REQUEST)
    response = JSONResponse(
            content={"Confirm": "Welcome!"},
            status_code=status.HTTP_200_OK)
    response.set_cookie(key='session_token')
    return response


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
