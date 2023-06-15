from typing import Optional

import strawberry

from fastgql.models import Task as TaskModel


@strawberry.experimental.pydantic.type(model=TaskModel, all_fields=True)
class Task:
    instance: strawberry.Private[TaskModel]

    @classmethod
    def from_instance(cls, instance: TaskModel) -> "Task":
        return cls(  # type: ignore[call-arg]
            instance=instance,
            id=instance.id,
            name=instance.name,
            description=instance.description,
            completed=instance.completed,
            created_at=instance.created_at,
            updated_at=instance.updated_at,
        )


@strawberry.experimental.pydantic.input(model=TaskModel)
class TaskInput:
    name: str
    description: Optional[str]

    def as_instance(self) -> TaskModel:
        return TaskModel(
            name=self.name,
            description=self.description,
        )
