from fastapi import FastAPI

from app.api.v1 import auth, health, lists, tasks


def create_app() -> FastAPI:
    app = FastAPI(title="Backend Challenge", version="0.1.0")

    app.include_router(health.router, prefix="/api/v1")
    app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
    app.include_router(lists.router, prefix="/api/v1/lists", tags=["lists"])
    app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["tasks"])

    return app


app = create_app()

