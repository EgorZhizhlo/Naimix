from sqlalchemy import select
from app.core import BaseDAO
from .models import Worker, Team, TeamMember
from app.core import async_session


class WorkerDAO(BaseDAO):
    model = Worker

    @classmethod
    async def find_in(cls, arr: list, **kwargs):
        async with async_session() as session:
            query = select(cls.model).where(
                cls.model.id.in_(arr)
            ).filter_by(**kwargs)
            result = await session.execute(query)
            return result.scalars().all()


class TeamDAO(BaseDAO):
    model = Team


class TeamMemberDAO(BaseDAO):
    model = TeamMember

    @classmethod
    async def find_in(cls, **kwargs):
        async with async_session() as session:
            query = select(
                Worker, Team
            ).join(
                TeamMember, TeamMember.team_id == Team.id
            ).join(
                Worker, TeamMember.worker_id == Worker.id
            ).filter_by(**kwargs)
            result = await session.execute(query)
            return result.all()
