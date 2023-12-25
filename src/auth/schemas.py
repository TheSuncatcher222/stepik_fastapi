"""
Модуль схем для валидации данных через Pydantic в модуле "auth".
"""

from pydantic import BaseModel, EmailStr, validator

NL: str = '\n'

# INFO: в pydantic.EmailStr разрешенные длины строк составляют 64@63.63
USER_EMAIL_MAX_LEN: int = 64 + 63 + 63
USER_HASH_PASS_LEN: int = 255

PASS_LEN_MAX: int = 50
PASS_LEN_MIN: int = 5
PASS_SPECIAL_CHARS: str = '!_@#$%^&+='

PASS_CHARS_VALIDATORS: dict[str, str] = {
    lambda s: PASS_LEN_MIN <= len(s) <= PASS_LEN_MAX: f'{NL}- длина от {PASS_LEN_MIN} до {PASS_LEN_MAX} символов',
    lambda s: any(char.isdigit() for char in s): '\n- включает хотя бы одну цифру (0-9)',
    lambda s: any(char.islower() for char in s): '\n- включает хотя бы одну прописную букву (a-z)',
    lambda s: any(char.isupper() for char in s): '\n- включает хотя бы одну заглавную букву (A-Z)',
    lambda s: any(char in PASS_SPECIAL_CHARS for char in s): f'{NL}- включает хотя бы один специальный символ ({PASS_SPECIAL_CHARS})',
}


class UserRegister(BaseModel):
    """Схема представления данных для регистрации пользователя."""

    email: EmailStr
    password: str

    @validator('email')
    def validate_email(cls, value):
        """Переводит символы поля email в нижний регистр."""
        return value.lower()

    @validator('password')
    def validate_password(cls, value):
        """Производит валидацию поля 'password'."""
        errors: list[str] = [
            err_message
            for condition, err_message
            in PASS_CHARS_VALIDATORS.items()
            if not condition(value)
        ]
        if len(errors) == 0:
            return value
        raise ValueError(
            'Введите пароль, который удовлетворяет критериям:' +
            ''.join(errors)
        )
