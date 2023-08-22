import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse

from core.core import check_age_grade
from db_fake import db_fake
from models.models import CalculateData, Users, UsersAgeGrade

app: FastAPI = FastAPI(title='My first FastAPI app')
db: list[Users] = db_fake


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


@app.get('/users/', response_model=list[UsersAgeGrade])
async def users_get():
    return db


@app.post('/users/', response_model=UsersAgeGrade)
async def users_post(user: Users):
    posted_user: UsersAgeGrade = UsersAgeGrade(
        id=user.id,
        name=user.name,
        age=user.age,
        age_grade=check_age_grade(age=user.age))
    db.append(posted_user)
    return posted_user


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
