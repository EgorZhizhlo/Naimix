import re
from pydantic import (
    BaseModel, EmailStr, Field,
    field_validator
)
from datetime import (
    date as d,
    time as t,
    datetime as dt,
)
from app.core import (
    IncorrectFormatException,
)


class CreateWorker(BaseModel):
    first_name: str = Field(
        ...,
        description='Имя сотрудника'
    )
    last_name: str = Field(
        ...,
        description='Фамилия сотрудника'
    )
    patronymic: str = Field(
        ...,
        description='Отчество сотрудника'
    )
    company_name: str = Field(
        ...,
        description='Компания сотрудника'
    )
    position: str = Field(
        ...,
        description='Должность сотрудника'
    )
    date_of_birth: d = Field(
        ...,
        description='Дата рождения сотрудника'
    )
    time_of_birth: t = Field(
        ...,
        default_factory=lambda: t(12, 0),
        description='Время рождения сотрудника'
    )
    addres_of_birth: str = Field(
        ...,
        description='Место рождения сотрудника'
    )

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, values: d):
        if values and values >= dt.now().date():
            raise IncorrectFormatException
        return values

    @field_validator("company_name")
    @classmethod
    def validate_company(cls, values: str):
        return values.lower()

    @field_validator("position")
    @classmethod
    def validate_position(cls, values: str):
        return values.lower()

    @field_validator('patronymic')
    @classmethod
    def validate_patronymic(cls, values: str):
        return values.lower()

    @field_validator("last_name")
    @classmethod
    def validate_last_name(cls, values: str):
        return values.lower()

    @field_validator("first_name")
    @classmethod
    def validate_first_name(cls, values: str):
        return values.lower()


class CreateTeam(BaseModel):
    team_name: str = Field(
        ...,
        description='Название команды'
    )

    @field_validator("team_name")
    @classmethod
    def validate_team_name(cls, values: str):
        return values.lower()


class AddWorkerToTeam(BaseModel):
    workers_id: list = Field(
        ...,
        description='ID работника(ов)'
    )
    team_id: int = Field(
        ...,
        description='ID команды'
    )


class WorkersIdList(BaseModel):
    workers_id: list = Field(
        ...,
        description='ID работника(ов)'
    )
