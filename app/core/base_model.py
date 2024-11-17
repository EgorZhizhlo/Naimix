from typing import Annotated
from datetime import (
    date as d,
    time as t,
    datetime as dt
)
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

from .config import create_database_url


database_url = create_database_url()
engine = create_async_engine(database_url)
async_session = async_sessionmaker(engine, expire_on_commit=False)


TEXT_NOT_NULL = Annotated[str, mapped_column(nullable=False)]
TEXT = Annotated[str, mapped_column(nullable=True)]
TEXT_NOT_NULL_UNIQUE = Annotated[
    str, mapped_column(nullable=False, unique=True)]
PK = Annotated[int, mapped_column(primary_key=True)]
INTEGER_NOT_NULL = Annotated[int, mapped_column(nullable=False)]
FLOAT_NOT_NULL = Annotated[float, mapped_column(nullable=False, default=0.0)]
TIME_NOT_NULL = Annotated[t, mapped_column(nullable=False)]
DATE_NOT_NULL = Annotated[d, mapped_column(nullable=False)]
BOOLEAN_DEFAULT_FALSE = Annotated[
    bool, mapped_column(default=False)]


class Base(AsyncAttrs, DeclarativeBase):
    id: Mapped[PK]
