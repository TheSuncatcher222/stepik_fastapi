from datetime import datetime
from enum import Enum

from pydantic import BaseModel

from auth.auth import password_hash
from core.core import set_age_grade


class ProductCategories(str, Enum):
    accessories = 'accessories'
    electronics = 'electronics'


PRODUCT_CATEGORIES_LIST: list[str] = [c.value for c in ProductCategories]


class ProductModel(BaseModel):
    id: int = None
    name: str
    category: ProductCategories
    price: float


class UsersAuthModel(BaseModel):
    username: str
    password: str


class UserRegisterModel(BaseModel):
    username: str
    password: str
    age: int


class UserModel(UserRegisterModel):
    id: int = None
    date_reg: datetime = datetime.utcnow()
    is_subscribed: bool = False
    age_grade: str = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.age_grade = set_age_grade(self.age)
        self.password: bytes = password_hash(self.password)


class UserWithoutPasswordModel(BaseModel):
    id: int
    username: str
    date_reg: datetime
    age: int
    age_grade: str
    is_subscribed: bool
