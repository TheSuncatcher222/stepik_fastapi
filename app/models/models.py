from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class ProductCategories(str, Enum):
    accessories = 'accessories'
    electronics = 'electronics'


PRODUCT_CATEGORIES_LIST: list[str] = [c.value for c in ProductCategories]


class Products(BaseModel):
    id: int = None
    name: str
    category: ProductCategories
    price: float


class Users(BaseModel):
    id: int = None
    name: str
    date_reg: datetime = datetime.utcnow()
    is_subscribed: bool = False
    age: int


class UsersAgeGrade(Users):
    age_grade: str
