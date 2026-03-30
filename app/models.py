import enum

from sqlalchemy import Column, Integer, String, Enum, DateTime
from datetime import datetime
from app.database import Base


class TaskStatus(enum.Enum):
    todo = 'todo'
    in_progress = 'in_progress'
    complete = 'complete'

class TaskPriority(enum.Enum):
    low = 'low'
    medium = 'medium'
    high = 'high'

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(String, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.todo)
    priority = Column(Enum(TaskPriority), default=TaskPriority.medium)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"Task(title={self.title}, status={self.status.value})"