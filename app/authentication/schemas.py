import re
from pydantic import (
    BaseModel, EmailStr, Field,
    field_validator
)
from datetime import (
    date as d,
    datetime as dt,
)
from app.core import (
    IncorrectFormatException,
)


class LoginModel(BaseModel):
    email: EmailStr = Field(
        ...,
        description='Электронная почта'
    )
    password: str = Field(
        ...,
        min_length=8,
        description='Пароль'
    )

    @field_validator('email')
    @classmethod
    def validate_phone_number(cls, values: str) -> str:
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', values):
            raise IncorrectFormatException
        return values.lower()


class RegistrationModel(LoginModel):
    first_name: str = Field(
        ...,
        description='Имя'
    )
    last_name: str = Field(
        ...,
        description='Фамилия'
    )
    company_name: str = Field(
        ...,
        description='Компания'
    )
    date_of_birth: d = Field(
        ...,
        description='Дата рождения'
    )
    phone_number: str = Field(
        ...,
        description='Номер телефона'
    )
    rep_password: str = Field(
        ...,
        min_length=8,
        description='Повтор пароля'
    )

    @field_validator('company_name')
    @classmethod
    def validate_company(cls, values: str) -> str:
        return values.lower()

    @field_validator('phone_number')
    @classmethod
    def validate_phone_number(cls, values: str) -> str:
        if not re.match(r'^\+\d{1,15}$', values):
            raise IncorrectFormatException
        return values

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, values: d):
        if values and values >= dt.now().date():
            raise IncorrectFormatException
        return values
