from typing import List

from sqlalchemy.orm import Session

from app.domain.schemas import ListCreate, ListRead, ListUpdate, ListWithCompletion
from app.infrastructure.db.repositories import ListRepository, TaskRepository


class ListService:
    def __init__(self, db: Session):
        self.db = db
        self.lists = ListRepository(db)
        self.tasks = TaskRepository(db)

    def create_list(self, payload: ListCreate) -> ListRead:
        todo_list = self.lists.create(
            name=payload.name,
            description=payload.description,
        )
        return ListRead.model_validate(todo_list)

    def list_lists(self) -> List[ListRead]:
        items = self.lists.list_all()
        return [ListRead.model_validate(item) for item in items]

    def get_list_with_completion(self, list_id: int) -> ListWithCompletion:
        todo_list = self.lists.get(list_id)
        completion = self.tasks.completion_percentage_for_list(list_id)
        data = ListWithCompletion(
            id=todo_list.id,
            name=todo_list.name,
            description=todo_list.description,
            completion_percentage=completion,
        )
        return data

    def update_list(self, list_id: int, payload: ListUpdate) -> ListRead:
        todo_list = self.lists.update(
            list_id=list_id,
            name=payload.name,
            description=payload.description,
        )
        return ListRead.model_validate(todo_list)

    def delete_list(self, list_id: int) -> None:
        self.lists.delete(list_id)

