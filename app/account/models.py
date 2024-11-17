from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core import (
    Base, TEXT, TEXT_NOT_NULL, TEXT_NOT_NULL_UNIQUE,
    DATE_NOT_NULL, TIME_NOT_NULL, FLOAT_NOT_NULL, TEXT
)


class Worker(Base):
    __tablename__ = "worker"

    first_name: Mapped[TEXT_NOT_NULL]
    last_name: Mapped[TEXT_NOT_NULL]
    patronymic: Mapped[TEXT_NOT_NULL]
    position: Mapped[TEXT_NOT_NULL]
    company_name: Mapped[TEXT_NOT_NULL]
    team_name: Mapped[TEXT]
    date_of_birth: Mapped[DATE_NOT_NULL]
    zodiac_sign: Mapped[TEXT_NOT_NULL]
    cosmogram_info: Mapped[TEXT_NOT_NULL]

    team_memberships = relationship("TeamMember", back_populates="worker")


class Team(Base):
    __tablename__ = "team"

    company_name: Mapped[TEXT_NOT_NULL]
    team_name: Mapped[TEXT_NOT_NULL]

    members = relationship("TeamMember", back_populates="team")


class TeamMember(Base):
    __tablename__ = "team_member"

    worker_id: Mapped[int] = mapped_column(
        ForeignKey("worker.id"), nullable=False)
    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"), nullable=False)
    similarity_coef: Mapped[FLOAT_NOT_NULL]

    worker = relationship("Worker", back_populates="team_memberships")
    team = relationship("Team", back_populates="members")
