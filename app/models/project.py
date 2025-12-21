from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    project_number = Column(Integer, unique=True, nullable=False)  # ← NEW: Display number
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(500), nullable=True)

    tasks = relationship(
        "Task",
        back_populates="project",
        cascade="all, delete-orphan"
    )