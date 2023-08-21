import uvicorn

from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app: FastAPI = FastAPI(title='My first FastAPI app')


class CalculateData(BaseModel):
    num1: int
    num2: int


@app.get('/')
async def index():
    with open(file='index.html',
              mode='r',
              encoding='utf-8') as html_file:
        html_content = html_file.read()
    return HTMLResponse(content=html_content, status_code=status.HTTP_200_OK)


@app.post('/calculate_path/')
async def calculate_path(num1: int, num2: int):
    return {"result": num1+num2}


@app.post('/calculate_body/')
async def calculate_body(data: CalculateData):
    return {"result": data.num1 + data.num2}

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
