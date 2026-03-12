from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.domain.enums import TaskPriority, TaskStatus
from app.infrastructure.db.base import Base


class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    tasks = relationship("Task", back_populates="assignee")


class TodoList(Base, TimestampMixin):
    __tablename__ = "todo_lists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)

    tasks = relationship(
        "Task",
        back_populates="todo_list",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Task(Base, TimestampMixin):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING, nullable=False)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False)
    due_date = Column(DateTime, nullable=True)

    list_id = Column(
        Integer,
        ForeignKey("todo_lists.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)

    todo_list = relationship("TodoList", back_populates="tasks")
    assignee = relationship("User", back_populates="tasks")

