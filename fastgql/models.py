from datetime import datetime
from typing import Optional, cast

from sqlmodel import Field, SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql.expression import Select


class TaskNotFound(Exception):
    """Task not found"""


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


async def complete_task(
    session: AsyncSession,
    task_id: int,
) -> Task:
    task = await session.get(Task, task_id)
    if task is None:
        raise TaskNotFound(f"Task with id {task_id} not found")
    task.completed = True
    await session.commit()
    await session.refresh(task)
    return task
