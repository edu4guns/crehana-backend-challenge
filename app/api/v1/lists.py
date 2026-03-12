from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.application.services.list_service import ListService, get_list_service
from app.domain.schemas import ListCreate, ListRead, ListUpdate, ListWithCompletion
from app.domain.exceptions import NotFoundError


router = APIRouter()


@router.post("/", response_model=ListRead, status_code=status.HTTP_201_CREATED)
def create_list(
    payload: ListCreate,
    service: ListService = Depends(get_list_service),
) -> ListRead:
    return service.create_list(payload)


@router.get("/", response_model=List[ListRead])
def list_lists(
    service: ListService = Depends(get_list_service),
) -> List[ListRead]:
    return service.list_lists()


@router.get("/{list_id}", response_model=ListWithCompletion)
def get_list(
    list_id: int,
    service: ListService = Depends(get_list_service),
) -> ListWithCompletion:
    try:
        return service.get_list_with_completion(list_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.put("/{list_id}", response_model=ListRead)
def update_list(
    list_id: int,
    payload: ListUpdate,
    service: ListService = Depends(get_list_service),
) -> ListRead:
    try:
        return service.update_list(list_id, payload)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_list(
    list_id: int,
    service: ListService = Depends(get_list_service),
) -> None:
    try:
        service.delete_list(list_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

