ADULT_AGE: int = 18
ADULT: str = 'adult'
MINOR: str = 'minor'

PRODUCTS: str = 'products'
USERS: str = 'users'


def check_age_grade(age: int) -> str:
    """Return age grade:
        - minor for age under 18;
        - adult in other case."""
    return ADULT if age >= ADULT_AGE else MINOR
