from fastapi import FastAPI, status
from fastapi.responses import FileResponse, HTMLResponse

from core.core import (
    PRODUCTS, USERS,
    check_age_grade)
from db_fake import DB_FAKE_INIT
from models.models import (
    PRODUCT_CATEGORIES_LIST,
    Products, Users, UsersAgeGrade)

app: FastAPI = FastAPI(title='My first FastAPI app')

db: dict[str, dict[int, any]] = DB_FAKE_INIT

@app.get('/')
async def index():
    with open(file='app/index.html',
              mode='r',
              encoding='utf-8') as html_file:
        html_content = html_file.read()
    return HTMLResponse(content=html_content, status_code=status.HTTP_200_OK)


@app.get('/download/')
async def download_requirements():
    return FileResponse(
        path='requirements.txt',
        filename='Project_Requirements.txt',
        status_code=status.HTTP_200_OK,
        media_type='text/txt')


@app.get('/products/', response_model=list[Products])
async def products_get(limit: int = 3, offset: int = 0):
    return list(db[PRODUCTS].values())[offset:limit+offset]


@app.get('/products/search/', response_model=list[Products] | dict)
async def products_get_search(
        keyword: str,
        category: str = None,
        limit: int = 10):
    if category and category not in PRODUCT_CATEGORIES_LIST:
        return {"BadRequest": "Category doesn't exist!"}
    response: list[Products] = list(
        filter(lambda product: keyword.lower() in product.name.lower(),
               db[PRODUCTS].values()))
    if category:
        response: list[Products] = list(
            filter(lambda product: category.lower() == product.category,
                   response))
    return response[:limit]


@app.get('/products/{id}/', response_model=Products | dict)
async def products_get_id(id: int):
    return db[PRODUCTS].get(id, {"BadRequest": "Product doesn't exist!"})


@app.post('/products/', response_model=Products)
async def products_post(product: Products):
    new_id: int = len(db[PRODUCTS]) + 1
    posted_product: Products = Products(
        id=new_id,
        name=product.name,
        category=product.category,
        price=product.price)
    db[PRODUCTS][new_id] = posted_product
    return posted_product


@app.get('/users/', response_model=list[UsersAgeGrade])
async def users_get(limit: int = 3, offset: int = 0):
    return list(db[USERS].values())[offset:limit+offset]


@app.post('/users/', response_model=UsersAgeGrade | dict)
async def users_post(user: Users):
    new_id: int = len(db[USERS]) + 1
    posted_user: UsersAgeGrade = UsersAgeGrade(
        id=new_id,
        name=user.name,
        age=user.age,
        age_grade=check_age_grade(age=user.age))
    db[USERS][new_id] = posted_user
    return posted_user


@app.get('/users/{id}/', response_model=UsersAgeGrade | dict)
async def users_get_id(id: int):
    return db[USERS].get(id, {"BadRequest": "User doesn't exist!"})


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
