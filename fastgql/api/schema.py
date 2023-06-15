import strawberry
from strawberry.extensions import Extension
from strawberry.types import Info

from fastgql.database import get_sessionmaker
from fastgql.models import add_task, complete_task, get_tasks

from .definitions.task import Task, TaskInput


class SQLModelSession(Extension):  # type: ignore[misc]
    def on_request_start(self) -> None:
        self.execution_context.context["session"] = get_sessionmaker()()

    def on_request_end(self) -> None:
        self.execution_context.context["session"].close()


@strawberry.type
class Query:
    @strawberry.field
    async def get_incomplete_tasks(self, info: Info, limit: int = 10) -> list[Task]:
        session = info.context["session"]
        tasks = await get_tasks(session, completed=False, limit=limit)
        return [Task.from_pydantic(task) for task in tasks]  # type: ignore[attr-defined]


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def add_task(self, info: Info, task: TaskInput) -> Task:
        session = info.context["session"]
        return Task.from_pydantic(await add_task(session, task.to_pydantic()))  # type: ignore[attr-defined, no-any-return]

    @strawberry.mutation
    async def complete_task(self, info: Info, task_id: int) -> Task:
        session = info.context["session"]
        return Task.from_pydantic(await complete_task(session, task_id))  # type: ignore[attr-defined, no-any-return]


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[SQLModelSession],
)
