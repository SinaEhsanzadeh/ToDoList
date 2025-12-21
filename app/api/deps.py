from typing import Any, Generator

from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.repositories.sqlalchemy import SQLTaskRepo, SQLProjectRepo
from app.services.task_service import TaskService
from app.services.project_service import ProjectService

def get_db() -> Generator[Any, Any, None]:
    """Dependency that provides a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_project_repo(db: Session = Depends(get_db)) -> SQLProjectRepo:
    """Dependency that provides a Project repository."""
    return SQLProjectRepo(db)

def get_task_repo(db: Session = Depends(get_db)) -> SQLTaskRepo:
    """Dependency that provides a Task repository."""
    return SQLTaskRepo(db)

def get_project_service(
    project_repo: SQLProjectRepo = Depends(get_project_repo)
)-> ProjectService:
    """Dependency that provides the Project service."""
    return ProjectService(project_repo)

def get_task_service(
    task_repo: SQLTaskRepo = Depends(get_task_repo),
    project_repo: SQLProjectRepo = Depends(get_project_repo)
) -> TaskService:
    """Dependency that provides the Task service."""
    return TaskService(task_repo, project_repo)