from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectRead
from app.services.project_service import ProjectService
from app.api.deps import get_project_service

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
    responses={404: {"description": "Project not found"}}
)

@router.post("/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(
        data: ProjectCreate,
        service: ProjectService = Depends(get_project_service)
):
    """
    Create a new project.

    Returns a project with a sequential **project_number**.
    Use this **project_number** in all subsequent API calls, not the internal ID.

    Example response:
    ```json
    {
      "id": 5,
      "project_number": 1,  # ← Use this in URLs
      "name": "My Project",
      "description": "Project description"
    }
    ```
    """
    try:
        project_id = service.create_project(data.name, data.description)
        return service.get_project(project_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[ProjectRead])
def list_projects(service: ProjectService = Depends(get_project_service)):
    """
    List all projects in sequential order.

    Projects are ordered by **project_number**, not internal ID.
    """
    return service.list_projects()


@router.get("/{project_number}", response_model=ProjectRead)
def get_project(
        project_number: int,
        service: ProjectService = Depends(get_project_service)
):
    """
    Get a project by its sequential number.

    - **project_number**: The sequential display number (1, 2, 3...)
    - Do not use the internal `id` field
    """
    try:
        return service.get_project_by_number(project_number)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{project_number}", response_model=ProjectRead)
def update_project(
        project_number: int,
        data: ProjectUpdate,
        service: ProjectService = Depends(get_project_service)
):
    """
    Update project details by sequential number.

    - **project_number**: The sequential display number
    """
    try:
        updates = {k: v for k, v in data.dict().items() if v is not None}
        service.update_project_by_number(project_number, **updates)
        return service.get_project_by_number(project_number)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{project_number}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
        project_number: int,
        service: ProjectService = Depends(get_project_service)
):
    """
    Delete a project by sequential number.

    - **project_number**: The sequential display number
    - All tasks in the project will be deleted (cascade)
    - Remaining projects will be renumbered to fill the gap
    """
    try:
        service.delete_project_by_number(project_number)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))