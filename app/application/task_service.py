from typing import List

from fastapi import BackgroundTasks
from sqlalchemy.orm import Session

from app.domain.enums import TaskStatus
from app.domain.exceptions import BusinessValidationError
from app.domain.schemas import TaskCreate, TaskFilters, TaskRead, TaskUpdate
from app.infrastructure.db.models import User
from app.infrastructure.db.repositories import ListRepository, TaskRepository, UserRepository


def _fake_send_email(to_email: str, task_id: int) -> None:
    # Simulación de envío de email (no real).
    print(f"Enviando email ficticio a {to_email} por asignación de tarea {task_id}")


class TaskService:
    def __init__(self, db: Session):
        self.db = db
        self.lists = ListRepository(db)
        self.tasks = TaskRepository(db)
        self.users = UserRepository(db)

    def _ensure_list_exists(self, list_id: int) -> None:
        self.lists.get(list_id)

    def create_task(
        self,
        list_id: int,
        payload: TaskCreate,
        background_tasks: BackgroundTasks | None = None,
    ) -> TaskRead:
        self._ensure_list_exists(list_id)
        assignee_id = payload.assignee_id
        if assignee_id is not None:
            self.users.get(assignee_id)
        task = self.tasks.create(
            list_id=list_id,
            title=payload.title,
            description=payload.description,
            priority=payload.priority,
            due_date=payload.due_date,
            assignee_id=assignee_id,
        )
        if assignee_id is not None and background_tasks is not None:
            user: User = self.users.get(assignee_id)
            background_tasks.add_task(_fake_send_email, user.email, task.id)
        return TaskRead.model_validate(task)

    def list_tasks(
        self,
        list_id: int,
        filters: TaskFilters | None = None,
    ) -> List[TaskRead]:
        self._ensure_list_exists(list_id)
        items = self.tasks.list_by_list(list_id, filters)
        return [TaskRead.model_validate(item) for item in items]

    def update_task(
        self,
        list_id: int,
        task_id: int,
        payload: TaskUpdate,
    ) -> TaskRead:
        if payload.assignee_id is not None:
            self.users.get(payload.assignee_id)

        task = self.tasks.update(
            list_id=list_id,
            task_id=task_id,
            title=payload.title,
            description=payload.description,
            priority=payload.priority,
            status=payload.status,
            assignee_id=payload.assignee_id,
            due_date=payload.due_date,
        )
        return TaskRead.model_validate(task)

    def change_status(
        self,
        list_id: int,
        task_id: int,
        new_status: TaskStatus,
    ) -> TaskRead:
        task = self.tasks.get(list_id, task_id)
        if new_status == TaskStatus.DONE and not task.title:
            raise BusinessValidationError("Una tarea completada debe tener título")
        task = self.tasks.change_status(list_id, task_id, new_status)
        return TaskRead.model_validate(task)

    def delete_task(self, list_id: int, task_id: int) -> None:
        self.tasks.delete(list_id, task_id)

    def assign_task(
        self,
        list_id: int,
        task_id: int,
        user_id: int,
        background_tasks: BackgroundTasks | None = None,
    ) -> TaskRead:
        user = self.users.get(user_id)
        task = self.tasks.update(
            list_id=list_id,
            task_id=task_id,
            assignee_id=user_id,
        )
        if background_tasks is not None:
            background_tasks.add_task(_fake_send_email, user.email, task.id)
        return TaskRead.model_validate(task)

