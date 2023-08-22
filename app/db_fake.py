from core.core import PRODUCTS, USERS, check_age_grade
from models.models import UsersAgeGrade

DB_FAKE_INIT: dict[str, dict[int, any]] = {
    PRODUCTS: {},
    USERS: {},}
