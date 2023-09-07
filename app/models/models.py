"""
Create models for project.

Models:
    - ProductModel: represent products data
                    uses ProductCategories to validate "category" field
    - UsersAuthModel: validate "username" and "password fields during user
                      authentication process to obtain JWT token
    - UserRegisterModel: validate "username", "password" and "age" fields
                         during user registration process
    - UserModel: collect all user data and hash password,
                 used to add user to db
    - UserWithoutPasswordModel: represent full user data without password

Auxiliary classes:
    - ProductCategories: represent list of valid product categories
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel

from auth.auth import password_hash
from core.core import set_age_grade


class ProductCategories(str, Enum):
    accessories = 'accessories'
    electronics = 'electronics'


class UserRoles(str, Enum):
    is_anonymous = 'is_anonymous'
    is_authenticated = 'is_authenticated'
    is_admin = 'is_admin'
    is_superuser = 'is_superuser'


PRODUCT_CATEGORIES_LIST: list[str] = [c.value for c in ProductCategories]
USER_ROLES_LIST: list[str] = [c.value for c in UserRoles]


class ProductModel(BaseModel):
    """
    Class represents product.

    Attributes:
        - id: int - primary key
        - name: str - product name
        - category: str - product category, validated by ProductCategories
        - priceL float - product price
    """
    id: int = None
    name: str
    category: ProductCategories
    price: float


class UsersAuthModel(BaseModel):
    """
    Class represents user model during authentication.

    Attributes:
        - username: str - user username
        - password: str - user password
    """
    username: str
    password: str


class UserRegisterModel(BaseModel):
    """
    Class represents user model during registration.

    Attributes:
        - username: str - user username to set
        - password: str - user password to set
        - age: int - user age to set
    """
    username: str
    password: str
    age: int


class UserModel(UserRegisterModel):
    """
    Class represents user model to add to db.
    Inherits from UserRegisterModel.

    Attributes:
        - id: str - user primary key
        - username: str - user username
        - password: str - user password
                        - password is being hashed
        - age: int - user age
        - date_reg: datetime - user date of registration
        - is_subscribed: bool - user is_subscription state (default is False)
        - age_grade: str - set user age grade according set_age_grade logic
        - role: str - role at the server, validated by UserRoles
    """
    id: int = None
    date_reg: datetime = datetime.utcnow()
    is_subscribed: bool = False
    age_grade: str = None
    role: UserRoles = UserRoles.is_authenticated

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.age_grade = set_age_grade(self.age)
        self.password: bytes = password_hash(self.password)


class UserWithoutPasswordModel(BaseModel):
    """
    Class represents user model without password field.
    I don't know how to inherit it from UserModel and remove "password" field.

    Attributes:
        - id: str - user primary key
        - username: str - user username
        - date_reg: datetime - user date of registration
        - age: int - user age
        - age_grade: str - user age grade
        - is_subscribed: bool - user is_subscription state
    """
    id: int
    username: str
    date_reg: datetime
    age: int
    age_grade: str
    is_subscribed: bool
