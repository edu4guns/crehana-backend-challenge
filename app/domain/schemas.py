from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.domain.enums import TaskPriority, TaskStatus


class ListBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=500)


class ListCreate(ListBase):
    pass


class ListUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=500)


class ListRead(ListBase):
    id: int

    class Config:
        from_attributes = True


class ListWithCompletion(ListRead):
    completion_percentage: float = 0.0


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    assignee_id: Optional[int] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None
    assignee_id: Optional[int] = None
    due_date: Optional[datetime] = None


class TaskRead(TaskBase):
    id: int
    status: TaskStatus
    list_id: int
    assignee_id: Optional[int] = None

    class Config:
        from_attributes = True


class TaskFilters(BaseModel):
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100)


class UserRead(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    sub: Optional[str] = None
    exp: Optional[datetime] = None


class TokenSettings(BaseModel):
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


def default_access_token_delta(settings: TokenSettings) -> timedelta:
    return timedelta(minutes=settings.access_token_expire_minutes)

