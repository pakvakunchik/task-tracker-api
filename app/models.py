from sqlalchemy import Column, Integer, String, Enum, DateTime
from datetime import datetime
from app.database import Base
from app.enum import TaskStatus, TaskPriority

class TaskModel(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(String, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.todo, nullable=False)
    priority = Column(Enum(TaskPriority), default=TaskPriority.medium, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.now)

    def __repr__(self):
        return f"Task(title={self.title}, status={self.status.value})"