from typing import Optional

import strawberry

from fastgql.models import Task as TaskModel


@strawberry.experimental.pydantic.type(TaskModel, all_fields=True)
class Task:
    pass


@strawberry.experimental.pydantic.input(TaskModel)
class TaskInput:
    name: str
    description: Optional[str] = None
