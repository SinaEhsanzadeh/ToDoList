import enum
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base


class Status(str, enum.Enum):
    todo = "todo"
    doing = "doing"
    done = "done"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    task_number = Column(Integer, nullable=False)  # ← NEW: Sequential per project
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    status = Column(Enum(Status), default=Status.todo, nullable=False)
    deadline = Column(DateTime, nullable=True)
    closed_at = Column(DateTime, nullable=True)

    project = relationship("Project", back_populates="tasks")

    __table_args__ = (
        UniqueConstraint('project_id', 'task_number', name='uq_project_task_number'),
    )