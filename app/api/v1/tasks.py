from typing import List as ListType, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, status

from app.application.services.task_service import TaskService
from app.domain.enums import TaskPriority, TaskStatus
from app.domain.exceptions import BusinessValidationError, NotFoundError
from app.domain.schemas import TaskCreate, TaskFilters, TaskRead, TaskUpdate
from app.infrastructure.auth.jwt import get_current_user
from app.infrastructure.db.base import get_db


router = APIRouter()


def get_task_service(db=Depends(get_db)) -> TaskService:
    return TaskService(db)


@router.post(
    "/lists/{list_id}/tasks",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    list_id: int,
    payload: TaskCreate,
    background_tasks: BackgroundTasks,
    service: TaskService = Depends(get_task_service),
    current_user=Depends(get_current_user),  # noqa: B008
) -> TaskRead:
    try:
        return service.create_task(list_id, payload, background_tasks)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/lists/{list_id}/tasks", response_model=ListType[TaskRead])
def list_tasks(
    list_id: int,
    status_filter: Optional[TaskStatus] = Query(default=None, alias="status"),
    priority_filter: Optional[TaskPriority] = Query(default=None, alias="priority"),
    service: TaskService = Depends(get_task_service),
    current_user=Depends(get_current_user),  # noqa: B008
) -> ListType[TaskRead]:
    filters = TaskFilters(status=status_filter, priority=priority_filter)
    try:
        return service.list_tasks(list_id, filters)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.put("/lists/{list_id}/tasks/{task_id}", response_model=TaskRead)
def update_task(
    list_id: int,
    task_id: int,
    payload: TaskUpdate,
    service: TaskService = Depends(get_task_service),
    current_user=Depends(get_current_user),  # noqa: B008
) -> TaskRead:
    try:
        return service.update_task(list_id, task_id, payload)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch(
    "/lists/{list_id}/tasks/{task_id}/status",
    response_model=TaskRead,
)
def change_status(
    list_id: int,
    task_id: int,
    new_status: TaskStatus,
    service: TaskService = Depends(get_task_service),
    current_user=Depends(get_current_user),  # noqa: B008
) -> TaskRead:
    try:
        return service.change_status(list_id, task_id, new_status)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except BusinessValidationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.delete(
    "/lists/{list_id}/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(
    list_id: int,
    task_id: int,
    service: TaskService = Depends(get_task_service),
    current_user=Depends(get_current_user),  # noqa: B008
) -> None:
    try:
        service.delete_task(list_id, task_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post(
    "/lists/{list_id}/tasks/{task_id}/assign",
    response_model=TaskRead,
)
def assign_task(
    list_id: int,
    task_id: int,
    user_id: int,
    background_tasks: BackgroundTasks,
    service: TaskService = Depends(get_task_service),
    current_user=Depends(get_current_user),  # noqa: B008
) -> TaskRead:
    try:
        return service.assign_task(list_id, task_id, user_id, background_tasks)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

