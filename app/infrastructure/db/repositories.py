from typing import Iterable, Optional

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.domain.enums import TaskStatus
from app.domain.exceptions import NotFoundError
from app.domain.schemas import TaskFilters
from app.infrastructure.db import models


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> Optional[models.User]:
        stmt = select(models.User).where(models.User.email == email)
        return self.db.scalar(stmt)

    def get(self, user_id: int) -> models.User:
        user = self.db.get(models.User, user_id)
        if not user:
            raise NotFoundError("Usuario no encontrado")
        return user

    def create(self, email: str, hashed_password: str) -> models.User:
        user = models.User(email=email, hashed_password=hashed_password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user


class ListRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str, description: Optional[str]) -> models.TodoList:
        todo_list = models.TodoList(name=name, description=description)
        self.db.add(todo_list)
        self.db.commit()
        self.db.refresh(todo_list)
        return todo_list

    def get(self, list_id: int) -> models.TodoList:
        todo_list = self.db.get(models.TodoList, list_id)
        if not todo_list:
            raise NotFoundError("Lista no encontrada")
        return todo_list

    def list_all(self) -> Iterable[models.TodoList]:
        stmt = select(models.TodoList).order_by(models.TodoList.id)
        return self.db.scalars(stmt).all()

    def update(
        self, list_id: int, name: Optional[str], description: Optional[str]
    ) -> models.TodoList:
        todo_list = self.get(list_id)
        if name is not None:
            todo_list.name = name
        if description is not None:
            todo_list.description = description
        self.db.commit()
        self.db.refresh(todo_list)
        return todo_list

    def delete(self, list_id: int) -> None:
        todo_list = self.get(list_id)
        self.db.delete(todo_list)
        self.db.commit()


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        list_id: int,
        title: str,
        description: Optional[str],
        priority,
        due_date,
        assignee_id: Optional[int],
    ) -> models.Task:
        task = models.Task(
            list_id=list_id,
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            assignee_id=assignee_id,
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get(self, list_id: int, task_id: int) -> models.Task:
        task = self.db.get(models.Task, task_id)
        if not task or task.list_id != list_id:
            raise NotFoundError("Tarea no encontrada")
        return task

    def list_by_list(
        self, list_id: int, filters: Optional[TaskFilters] = None
    ) -> Iterable[models.Task]:
        conditions = [models.Task.list_id == list_id]
        if filters:
            if filters.status:
                conditions.append(models.Task.status == filters.status)
            if filters.priority:
                conditions.append(models.Task.priority == filters.priority)

        stmt = select(models.Task).where(and_(*conditions)).order_by(models.Task.id)
        return self.db.scalars(stmt).all()

    def update(
        self,
        list_id: int,
        task_id: int,
        **fields,
    ) -> models.Task:
        task = self.get(list_id, task_id)
        for key, value in fields.items():
            if value is not None:
                setattr(task, key, value)
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, list_id: int, task_id: int) -> None:
        task = self.get(list_id, task_id)
        self.db.delete(task)
        self.db.commit()

    def change_status(
        self,
        list_id: int,
        task_id: int,
        new_status: TaskStatus,
    ) -> models.Task:
        return self.update(list_id, task_id, status=new_status)

    def completion_percentage_for_list(self, list_id: int) -> float:
        tasks = self.list_by_list(list_id, None)
        total = len(tasks)
        if total == 0:
            return 0.0
        done = len([t for t in tasks if t.status == TaskStatus.DONE])
        return round(done * 100.0 / total, 2)

