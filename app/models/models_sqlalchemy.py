"""
Create models for database.

Models:
    - User: represents user data
    - Item: represent item data, foreign key to User
"""

from datetime import date
from enum import Enum

from re import fullmatch

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, relationship, validates

from app.auth.auth import password_hash
from app.database import Base, session


"""Users data."""


class UserAgeGrades(str, Enum):
    child = 'child'       # 0-17 age
    adult = 'adult'       # 18-60 age
    senior = 'senior'     # 61+ age


class UserRoles(str, Enum):
    is_anonymous = 'is_anonymous'
    is_authenticated = 'is_authenticated'
    is_admin = 'is_admin'
    is_superuser = 'is_superuser'


USER_AGE_MAX_CHILD: int = 17
USER_AGE_MAX_ADULT: int = 60

USERS_AGE_GRADES: list[str] = [c.value for c in UserAgeGrades]
USER_ROLES: list[str] = [c.value for c in UserRoles]

AGE_RANGE: range = range(1, 151)
AGE_RANGE_ERROR: str = 'Please enter correct age between 1 and 150.'
EMAIL_PATTERN: str = r'^(?!\.)[0-9a-zA-Z\.]{1,50}@[a-zA-z]+\.[a-zA-z]+$'
EMAIL_PATTERN_ERROR: str = (
    'Please enter correct email address (e.g. "valid@email.com")!')
PASS_PATTERN: str = (
    r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!_@#$%^&+=]).{6,50}$')
PASS_PATTERN_ERROR: str = (
    'Please enter password that meets the following criteria:\n'
    '    - the length must be between 6 and 50 characters;\n'
    '    - must contain at least one digit (0-9);\n'
    '    - must contain at least one lowercase letter (a-z);\n'
    '    - must contain at least one uppercase letter (A-Z);\n'
    '    - must contain at least one special character.')
USERNAME_PATTERN: str = r'^[0-9a-zA-Z]{6,30}$'
USERNAME_PATTERN_ERROR: str = (
    'Please enter username that meets the following criteria:\n'
    '    - the length must be between 6 and 30 characters;\n'
    '    - only digits (0-9) or letters (a-z)/(A-Z) are allowed.')
USERNAME_UNIQUE_ERROR: str = ('Username is already taken!')


"""Items data."""


class ItemCategories(str, Enum):
    automotive = 'Automotive'
    baby_and_kids = 'Baby and Kids'
    beauty_and_personal_care = 'Beauty and Personal Care'
    books_and_entertainment = 'Books and Entertainment'
    clothing_and_footwear = 'Clothing and Footwear'
    electronics = 'Electronics'
    food_and_beverages = 'Food and Beverages'
    home_and_garden = 'Home and Garden'
    pet_supplies = 'Pet Supplies'
    sports_and_fitness = 'Sports and Fitness'


ITEM_CATEGORIES: list[str] = [c.value for c in ItemCategories]
ITEM_CATEGORIES_STR: str = ", ".join(
        ITEM_CATEGORIES[index] for index in range(len(ITEM_CATEGORIES)))

NAME_PATTERN: str = r'^[0-9A-Za-z]{6,30}$'
NAME_PATTERN_ERROR: str = (
    'Please enter name that meets the following criteria:\n'
    '    - the length must be between 6 and 30 characters;\n'
    '    - only digits (0-9) or letters (a-z)/(A-Z) are allowed.')
CATEGORY_ERROR: str = f'Category must be in: {ITEM_CATEGORIES_STR}.'
DESCRIPTION_RANGE: range = range(1, 101)
DESCRIPTION_RANGE_ERROR: str = (
    'Description length must be between 1-100 characters.')
PRICE_ERROR: str = 'Price must be under 0.'


"""Models."""


class Item(Base):
    """
    Class represents items.

    Attributes:
        - id: int - primary key
        - name: str - item name
        - category: str - item category, validated by ItemCategories
        - price: float - item price
        - owner_id: int - foreign key to User model, CASCADE delete
        - owner: SQLAlchemy ORM relationship to User model

    Validations:
        # TODO: complete next time! 
    """
    __tablename__ = 'items'

    id: int = mapped_column(primary_key=True)
    name: str = mapped_column()
    category: str = mapped_column()
    description: str = mapped_column(nullable=True)
    price: float = mapped_column()
    owner_id = mapped_column(
        ForeignKey(
            column='users.items',
            ondelete='CASCADE'))

    owner = relationship('User', back_populates='items')

    @validates('name')
    def validate_name(self, key, value):
        """Validate name."""
        if fullmatch(NAME_PATTERN, value) is None:
            raise ValueError(NAME_PATTERN_ERROR)
        return value

    @validates('category')
    def validate_category(self, key, value):
        """Validate category."""
        if value not in ITEM_CATEGORIES:
            raise ValueError(CATEGORY_ERROR)
        return value

    @validates('description')
    def validate_description(self, key, value):
        """Validate description."""
        if value is not None and len(value) not in DESCRIPTION_RANGE:
            raise ValueError(DESCRIPTION_RANGE_ERROR)
        return value

    @validates('price')
    def validate_price(self, key, value):
        """Validate price."""
        if value <= 0:
            raise ValueError(PRICE_ERROR)
        return value


class User(Base):
    """
    Class represents users.

    Attributes:
        # TODO: complete next time!
    """
    __tablename__ = 'users'

    id: int = mapped_column(primary_key=True)
    username: str = mapped_column(index=True)
    email: str = mapped_column(unique=True)
    password: str = mapped_column()
    age: int = mapped_column()
    age_grade: str = mapped_column()
    date_reg: str = mapped_column()
    is_subscribed: bool = mapped_column(default=False)
    is_active: bool = mapped_column(default=True)
    role: UserRoles = mapped_column(default=UserRoles.is_authenticated)

    _username_lower: str = mapped_column()

    items = relationship('Item', back_populates='owner')

    @property
    def set_age_grade(self):
        """Set age_grade according to age value."""
        if self.age <= USER_AGE_MAX_CHILD:
            return UserAgeGrades.child
        elif self.age <= USER_AGE_MAX_ADULT:
            return UserAgeGrades.adult
        else:
            return UserAgeGrades.senior

    @property
    def set_date_reg(self):
        """Set current date (YYYY-MM-DD) to date_reg in str type."""
        return str(date.today())

    @validates('age')
    def validate_age(self, key, value):
        """Validate age."""
        if value not in AGE_RANGE:
            raise ValueError(AGE_RANGE_ERROR)
        return value

    @validates('email')
    def validate_email(self, key, value):
        """Validate and then lower email."""
        if fullmatch(EMAIL_PATTERN, value) is None:
            raise ValueError(EMAIL_PATTERN_ERROR)
        return value.lower()

    @validates('password')
    def validate_password(self, key, value):
        """Validate and then hash password."""
        if fullmatch(PASS_PATTERN, value) is None:
            raise ValueError(PASS_PATTERN_ERROR)
        return password_hash(value)

    @validates('username')
    def validate_username(self, key, value):
        """Validate username."""
        if fullmatch(USERNAME_PATTERN, value) is None:
            raise ValueError(USERNAME_PATTERN_ERROR)
        username_lower: str = value.lower()
        # TODO: какой тип возвращается?
        if_exists: any = session.query(User).filter(
            User._username_lower == username_lower)
        if if_exists:
            raise ValueError(USERNAME_UNIQUE_ERROR)
        self._username_lower: str = username_lower
        return value
