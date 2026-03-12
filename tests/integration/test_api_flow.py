from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.infrastructure.db.base import Base, get_db


def override_get_db():
    engine = create_engine("sqlite:///:memory:", future=True)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_full_todo_flow_without_auth():
    # Registro y login para obtener token
    resp = client.post(
        "/api/v1/auth/register",
        json={"email": "user@example.com", "password": "secret123"},
    )
    assert resp.status_code == 201

    resp = client.post(
        "/api/v1/auth/login",
        data={"username": "user@example.com", "password": "secret123"},
    )
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Crear lista
    resp = client.post(
        "/api/v1/lists",
        json={"name": "Mi lista", "description": "desc"},
        headers=headers,
    )
    assert resp.status_code == 201
    list_id = resp.json()["id"]

    # Crear tarea
    resp = client.post(
        f"/api/v1/tasks/lists/{list_id}/tasks",
        json={
            "title": "Tarea 1",
            "description": "d",
            "priority": "MEDIUM",
            "due_date": None,
            "assignee_id": None,
        },
        headers=headers,
    )
    assert resp.status_code == 201
    task_id = resp.json()["id"]

    # Cambiar estado
    resp = client.patch(
        f"/api/v1/tasks/lists/{list_id}/tasks/{task_id}/status",
        params={"new_status": "DONE"},
        headers=headers,
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "DONE"

    # Obtener lista con porcentaje de completitud
    resp = client.get(f"/api/v1/lists/{list_id}", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["completion_percentage"] == 100.0

