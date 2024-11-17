from sqlalchemy.orm import Mapped
from app.core import (
    Base, TEXT_NOT_NULL, TEXT_NOT_NULL_UNIQUE,
    DATE_NOT_NULL
)


class User(Base):
    __tablename__ = "user"

    first_name: Mapped[TEXT_NOT_NULL]
    last_name: Mapped[TEXT_NOT_NULL]
    company_name: Mapped[TEXT_NOT_NULL]
    date_of_birth: Mapped[DATE_NOT_NULL]
    email: Mapped[TEXT_NOT_NULL_UNIQUE]
    phone_number: Mapped[TEXT_NOT_NULL_UNIQUE]
    password: Mapped[TEXT_NOT_NULL]

    extend_existing = True
