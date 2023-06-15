from datetime import datetime
from typing import Optional, cast

from sqlmodel import Field, SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql.expression import Select


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


async def get_tasks(
    session: AsyncSession,
    completed: Optional[bool] = None,
    limit: Optional[int] = None,
) -> list[Task]:
    query = cast(Select[Task], select(Task))
    if completed is not None:
        query = query.where(Task.completed == completed)
    if limit is not None:
        query = query.limit(limit)
    results = await session.exec(query)
    return results.fetchall()


async def add_task(
    session: AsyncSession,
    task: Task,
) -> Task:
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task
