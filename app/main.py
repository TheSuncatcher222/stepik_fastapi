import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse

from core.core import check_age_grade
from models.models import CalculateData, Users

app: FastAPI = FastAPI(title='My first FastAPI app')


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


@app.post('/users/')
async def users_get(user: Users):
    posted_user: Users = Users(id=user.id,
                               name=user.name,
                               age=user.age)
    return {'id': posted_user.id,
            'name': posted_user.name,
            'age': posted_user.age,
            'date_reg': posted_user.date_reg,
            'status': check_age_grade(age=posted_user.age)}


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
