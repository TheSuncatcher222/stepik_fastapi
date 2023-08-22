from datetime import datetime

from pydantic import BaseModel


class CalculateData(BaseModel):
    num1: int
    num2: int


class Feedbacks(BaseModel):
    name: str
    message: str


class Users(BaseModel):
    id: int
    name: str
    date_reg: datetime = datetime.utcnow()
    age: int


class UsersAgeGrade(Users):
    age_grade: str
