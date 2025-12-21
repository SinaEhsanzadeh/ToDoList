from fastapi import APIRouter, Depends, HTTPException, status, Path
from typing import List
from app.schemas.task import TaskCreate, TaskUpdate, TaskRead
from app.services.task_service import TaskService
from app.api.deps import get_task_service

router = APIRouter(prefix="/projects/{project_number}/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    project_number: int = Path(..., gt=0, description="Project sequential number"),
    data: TaskCreate = ...,
    service: TaskService = Depends(get_task_service)
):
    """Create a new task in a project (using project sequential number)."""
    try:
        task_id = service.create_task_by_project_number(
            title=data.title,
            project_number=project_number,
            deadline=data.deadline
        )
        task = service.get_task(task_id)
        return task
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[TaskRead])
def list_tasks(
    project_number: int = Path(..., gt=0, description="Project sequential number"),
    service: TaskService = Depends(get_task_service)
):
    """List all tasks in a project (using project sequential number)."""
    try:
        return service.list_tasks_by_project_number(project_number)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{task_number}", response_model=TaskRead)
def get_task(
    project_number: int = Path(..., gt=0, description="Project sequential number"),
    task_number: int = Path(..., gt=0, description="Task number within project"),
    service: TaskService = Depends(get_task_service)
):
    """Get a task by project sequential number and task number."""
    try:
        return service.get_task_by_numbers(project_number, task_number)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{task_number}", response_model=TaskRead)
def update_task(
    project_number: int = Path(..., gt=0, description="Project sequential number"),
    task_number: int = Path(..., gt=0, description="Task number within project"),
    data: TaskUpdate = ...,
    service: TaskService = Depends(get_task_service)
):
    """Update task details by project sequential number and task number."""
    try:
        # Get non-None values
        updates = {k: v for k, v in data.dict().items() if v is not None}
        service.update_task_by_numbers(project_number, task_number, **updates)
        return service.get_task_by_numbers(project_number, task_number)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{task_number}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    project_number: int = Path(..., gt=0, description="Project sequential number"),
    task_number: int = Path(..., gt=0, description="Task number within project"),
    service: TaskService = Depends(get_task_service)
):
    """Delete a task by project sequential number and task number."""
    try:
        service.delete_task_by_numbers(project_number, task_number)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))