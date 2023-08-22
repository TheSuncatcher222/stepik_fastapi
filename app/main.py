import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import FileResponse, HTMLResponse

from core.core import check_age_grade
from db_fake import db_fake
from models.models import Feedbacks, CalculateData, Users, UsersAgeGrade

app: FastAPI = FastAPI(title='My first FastAPI app')
db: list[Users] = db_fake
db_id_hash: dict[int, int] = {}


@app.post('/calculate_path/')
async def calculate_path(num1: int, num2: int):
    return {"result": num1+num2}


@app.post('/calculate_body/')
async def calculate_body(data: CalculateData):
    return {"result": data.num1 + data.num2}


@app.get('/download/')
async def download_requirements():
    return FileResponse(
        path='requirements.txt',
        filename='Project_Requirements.txt',
        status_code=status.HTTP_200_OK,
        media_type='text/txt')


@app.post('/feedback/')
async def feedback_post(feedback: Feedbacks):
    return {"message": f"Feedback received. Thank you, {feedback.name}!"}


@app.get('/')
async def index():
    with open(file='app/index.html',
              mode='r',
              encoding='utf-8') as html_file:
        html_content = html_file.read()
    return HTMLResponse(content=html_content, status_code=status.HTTP_200_OK)


@app.get('/users/', response_model=list[UsersAgeGrade])
async def users_get(limit: int = 3, offset: int = 0):
    return db[offset:limit+offset]


@app.post('/users/', response_model=UsersAgeGrade | dict)
async def users_post(user: Users):
    if user.id in db_id_hash:
        return {"InternalError": "This Id is already exists!"}
    posted_user: UsersAgeGrade = UsersAgeGrade(
        id=user.id,
        name=user.name,
        age=user.age,
        age_grade=check_age_grade(age=user.age))
    db.append(posted_user)
    db_id_hash[user.id] = len(db)-1
    return posted_user


@app.get('/users/{id}/', response_model=UsersAgeGrade | dict)
async def users_get_id(id: int):
    hashed_id: int = db_id_hash.get(id)
    if hashed_id is not None:
        return db[hashed_id]
    return {"InternalError": "User doesn't exist!"}


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
