from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.application.services.task_service import TaskService
from app.domain.enums import TaskPriority, TaskStatus
from app.domain.schemas import TaskCreate, TaskUpdate
from app.infrastructure.db.base import Base
from app.infrastructure.db.models import Task, TodoList, User


def create_in_memory_session() -> Session:
    engine = create_engine("sqlite:///:memory:", future=True)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
    Base.metadata.create_all(bind=engine)
    return TestingSessionLocal()


def seed_list_and_user(db: Session) -> tuple[TodoList, User]:
    todo_list = TodoList(name="L", description=None)
    user = User(email="user@example.com", hashed_password="x", is_active=True)
    db.add_all([todo_list, user])
    db.commit()
    db.refresh(todo_list)
    db.refresh(user)
    return todo_list, user


def test_create_task_in_list():
    db = create_in_memory_session()
    todo_list, _ = seed_list_and_user(db)

    service = TaskService(db)

    task = service.create_task(
        list_id=todo_list.id,
        payload=TaskCreate(
            title="T1",
            description="desc",
            priority=TaskPriority.HIGH,
            due_date=None,
            assignee_id=None,
        ),
        background_tasks=None,
    )
    assert task.id is not None
    assert task.list_id == todo_list.id
    assert task.priority == TaskPriority.HIGH


def test_change_status_to_done():
    db = create_in_memory_session()
    todo_list, _ = seed_list_and_user(db)

    task = Task(title="T", description=None, list_id=todo_list.id)
    db.add(task)
    db.commit()
    db.refresh(task)

    service = TaskService(db)
    updated = service.change_status(todo_list.id, task.id, TaskStatus.DONE)
    assert updated.status == TaskStatus.DONE


def test_update_task_priority_and_assignee():
    db = create_in_memory_session()
    todo_list, user = seed_list_and_user(db)

    task = Task(title="T", description=None, list_id=todo_list.id)
    db.add(task)
    db.commit()
    db.refresh(task)

    service = TaskService(db)
    updated = service.update_task(
        todo_list.id,
        task.id,
        TaskUpdate(priority=TaskPriority.LOW, assignee_id=user.id),
    )
    assert updated.priority == TaskPriority.LOW
    assert updated.assignee_id == user.id

