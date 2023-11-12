"""
Create pydantic models for validation.

Models:
    - ProductModel: represents products data
                    uses ProductCategories to validate "category" field
    - UsersAuthModel: validates "username" and "password fields during user
                      authentication process to obtain JWT token
    - UserRegisterModel: validates "username", "password" and "age" fields
                         during user registration process
    - UserModel: collects all user data and hash password,
                 used to add user to db
    - UserWithoutPasswordModel: represents full user data without password

Auxiliary classes:
    - ProductCategories: represent list of valid product categories
"""

from datetime import datetime

from pydantic import BaseModel

from auth.auth import password_hash
from core.core import set_age_grade
from app.models.models_sqlalchemy import ItemCategories


class ItemBase(BaseModel):
    """
    Class represents items validation by Pydantic.

    Attributes:
        - name: str - item name
        - category: str - item category, validated by ItemCategories
        - description: str | None - OPTIONAL item description
        - price: float - item price
    """
    name: str
    category: ItemCategories
    description: str | None = None
    price: float


class Item(ItemBase):
    """
    Class represents items validation by Pydantic.

    Add attributes:
        - id: int - primary key
    """
    id: int


class ItemSingle(Item):
    """
    Class represents single item validation by Pydantic.

    Add attributes:
        - owner_id: int - item owner primary key in Users model
    """
    owner_id: int


class UsersLogIn(BaseModel):
    """
    Class represents user validation during login.

    Attributes:
        - username: str - user username
        - password: str - user password
    """
    username: str
    password: str


class UserRegister(BaseModel):
    """
    Class represents user validation during registration.

    Attributes:
        - username: str - user username to set
        - email: str - user email to set
        - password: str - user password to set
        - password_confirm: str - password confirm
        - age: int - user age to set
    """
    username: str
    email: str
    password: str
    password_confirm: str
    age: int


class UserRepresent(BaseModel):
    """
    Class represents user validation without password field.
    I don't know how to inherit it from UserModel and remove "password" field.

    Attributes:
        - id: str - user primary key
        - username: str - user username
        - email: str - user email
        - age: int - user age
        - age_grade: str - user age grade
        - date_reg: datetime - user date of registration
        - is_subscribed: bool - user is_subscription state
        - items: list[ItemsModel] - user items list from Item model
    """
    id: int
    username: str
    email: str
    age: int
    age_grade: str
    date_reg: datetime
    is_subscribed: bool
    items: list[Item]
