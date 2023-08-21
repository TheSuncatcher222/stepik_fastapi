ADULT: str = 'adult'
MINOR: str = 'minor'


def check_age_grade(age: int) -> str:
    """Return age grade:
        - minor for age under 18;
        - adult in other case."""
    return ADULT if age >= 18 else MINOR
