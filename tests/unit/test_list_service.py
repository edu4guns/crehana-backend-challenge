from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.application.services.list_service import ListService
from app.domain.schemas import ListCreate
from app.infrastructure.db.base import Base
from app.infrastructure.db.models import Task, TodoList


def create_in_memory_session() -> Session:
    engine = create_engine("sqlite:///:memory:", future=True)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
    Base.metadata.create_all(bind=engine)
    return TestingSessionLocal()


def test_create_and_get_list_with_completion():
    db = create_in_memory_session()
    service = ListService(db)

    # Crear lista
    created = service.create_list(ListCreate(name="Lista A", description="desc"))
    assert created.id is not None
    assert created.name == "Lista A"

    # Sin tareas, completitud debe ser 0
    with_completion = service.get_list_with_completion(created.id)
    assert with_completion.completion_percentage == 0.0


def test_list_lists_returns_all():
    db = create_in_memory_session()
    service = ListService(db)

    service.create_list(ListCreate(name="L1", description=None))
    service.create_list(ListCreate(name="L2", description=None))

    result = service.list_lists()
    assert len(result) == 2


def test_completion_percentage_with_tasks_done():
    db = create_in_memory_session()
    Base.metadata.create_all(bind=db.get_bind())

    # Crear lista y tareas manualmente
    todo_list = TodoList(name="L", description=None)
    db.add(todo_list)
    db.flush()

    task1 = Task(title="T1", list_id=todo_list.id)
    task2 = Task(title="T2", list_id=todo_list.id)
    task2.status = task2.status.DONE  # type: ignore[attr-defined]
    db.add_all([task1, task2])
    db.commit()

    service = ListService(db)
    result = service.get_list_with_completion(todo_list.id)
    assert result.completion_percentage == 50.0

