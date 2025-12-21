from typing import List, Optional

class ProjectService:
    def __init__(self, repo):
        self.repo = repo

    def create_project(self, name: str, description: str = None) -> int:
        """Create a new project and return its ID."""
        if not name or len(name.strip()) == 0:
            raise ValueError("Project name cannot be empty")

        return self.repo.add({
            "name": name.strip(),
            "description": description
        })

    def get_project(self, project_id: int):
        """Retrieve a single project by ID."""
        project = self.repo.get(project_id)
        if not project:
            raise ValueError(f"Project with ID {project_id} not found")
        return project

    def list_projects(self) -> List:
        """Retrieve all projects."""
        return self.repo.list_all()

    def update_project(self, project_id: int, name: str = None, description: str = None):
        """Update project details."""
        updates = {}
        if name is not None:
            if len(name.strip()) == 0:
                raise ValueError("Project name cannot be empty")
            updates["name"] = name.strip()
        if description is not None:
            updates["description"] = description

        if not updates:
            raise ValueError("No update data provided")

        self.repo.update(project_id, updates)

    def delete_project(self, project_id: int):
        """Delete a project (cascades to tasks)."""
        self.repo.delete(project_id)

    def get_project_by_number(self, project_number: int):
        """Get project by its sequential display number."""
        project = self.repo.get_by_number(project_number)
        if not project:
            raise ValueError(f"Project #{project_number} not found")
        return project

    def update_project_by_number(self, project_number: int, **updates):
        """Update project by its sequential display number."""
        project = self.get_project_by_number(project_number)
        self.update_project(project.id, **updates)

    def delete_project_by_number(self, project_number: int):
        """Delete project by its sequential display number."""
        project = self.get_project_by_number(project_number)
        self.delete_project(project.id)

    def list_projects_by_number(self):
        """List all projects ordered by their sequential number."""
        return self.repo.list_all_by_number()