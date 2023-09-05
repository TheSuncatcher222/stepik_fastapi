"""
Contain some useful examples.
"""

from datetime import datetime
from typing import Annotated

from fastapi import (
    FastAPI, HTTPException, Response, status,
    Cookie, Header)
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.security import OAuth2PasswordBearer

from core.core import PRODUCTS
from db_fake import DB_FAKE_INIT
from models.models import (PRODUCT_CATEGORIES_LIST, ProductModel)


app: FastAPI = FastAPI(title='My first FastAPI app')
oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl='token')

db: dict[str, dict[int, any]] = DB_FAKE_INIT


@app.get('/')
async def index(response: Response):
    """Return HTMLResponse with index.html file."""
    with open(file='app/index.html',
              mode='r',
              encoding='utf-8') as html_file:
        html_content = html_file.read()
    return HTMLResponse(content=html_content, status_code=status.HTTP_200_OK)


@app.post('/cookie/read/')
async def index_cookie_read(last_visit=Cookie()):
    """Read cookie data."""
    return {"last visit": last_visit}


@app.post('/cookie/set/')
async def index_cookie_set(response: Response):
    """Set cookie data."""
    now = datetime.now()
    response.set_cookie(key="last_visit", value=now)
    return {"message": "Cookies set!"}


@app.get('/download/')
async def download_requirements():
    """Return FileResponse with .txt file."""
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
    """Read header data of the request."""
    required_headers: dict[str, str | list[str]] = {
        'Accept-Language': accept_language,
        'Authorization': authorization,
        'User-Agent': user_agent}
    missing_headers: list[str] = [
        header for header, value in required_headers.items() if value is None]
    if missing_headers:
        raise HTTPException(
            detail=missing_headers,
            status_code=status.HTTP_401_UNAUTHORIZED)
    return JSONResponse(
        content=required_headers,
        status_code=status.HTTP_200_OK)


@app.get('/products/search/', response_model=list[ProductModel])
async def products_get_search(
        keyword: str,
        category: str = None,
        limit: int = 10):
    """Return objects matched the query."""
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
