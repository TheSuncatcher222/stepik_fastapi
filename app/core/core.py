"""
Contain project core data.
"""

from fastapi import HTTPException, status

ADULT_AGE: int = 18
ADULT: str = 'adult'
MINOR: str = 'minor'

PRODUCTS: str = 'products'
USERS: str = 'users'
USERS_USERNAMES: str = 'users_usernames'

STRTIME_FORMAT: str = '%Y-%m-%d %H:%M:%S'

HTTPEXCEPTION_401: HTTPException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Unauthorized',
    headers={"WWW-Authenticate": "Bearer"}) 


def set_age_grade(age: int) -> str:
    """Return age grade:
        - minor for age under 18;
        - adult in other case."""
    return ADULT if age >= ADULT_AGE else MINOR
