import pytest
from app.services.task_service import TaskService
from app.repositories.in_memory import InMemoryTaskRepo, InMemoryProjectRepo
from app.models.task import Status

def setup_service():
    project_repo = InMemoryProjectRepo()
    task_repo = InMemoryTaskRepo()
    service = TaskService(task_repo, project_repo)
    project_id = project_repo.add({"name": "Test"})
    return service, project_id

def test_create_task():
    service, project_id = setup_service()
    task_id = service.create_task("Test task", project_id)
    assert task_id == 1

def test_task_limit():
    service, project_id = setup_service()
    for i in range(10):
        service.create_task(f"Task {i}", project_id)
    with pytest.raises(ValueError):
        service.create_task("Overflow", project_id)

def test_close_task():
    service, project_id = setup_service()
    task_id = service.create_task("Close me", project_id)
    service.update_status(task_id, Status.done)

