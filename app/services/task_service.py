from typing import List, Optional
from datetime import datetime
import os
from dotenv import load_dotenv
from app.models.task import Status

load_dotenv()
MAX_TASKS = int(os.getenv("MAX_NUMBER_OF_TASKS", 10))

class TaskService:
    def __init__(self, task_repo, project_repo):
        self.task_repo = task_repo
        self.project_repo = project_repo

    def create_task(self, title: str, project_id: int, deadline: Optional[datetime] = None) -> int:
        """Create a new task and return its ID."""
        if not self.project_repo.get(project_id):
            raise ValueError("Project does not exist")

        if len(self.task_repo.list_by_project(project_id)) >= MAX_TASKS:
            raise ValueError(f"Task limit reached (max {MAX_TASKS})")

        if not title or len(title.strip()) == 0:
            raise ValueError("Task title cannot be empty")

        # Ensure deadline is None or a proper datetime
        if deadline and not isinstance(deadline, datetime):
            raise ValueError("Deadline must be a valid datetime object")

        return self.task_repo.add({
            "title": title.strip(),
            "project_id": project_id,
            "deadline": deadline,
            "status": Status.todo
        })

    def get_task(self, task_id: int):
        """Retrieve a single task by global ID."""
        task = self.task_repo.get(task_id)
        if not task:
            raise ValueError(f"Task with ID {task_id} not found")
        return task

    def get_task_by_number(self, project_id: int, task_number: int):
        """Retrieve a task by project ID and task number."""
        if not self.project_repo.get(project_id):
            raise ValueError("Project does not exist")

        task = self.task_repo.get_by_number(project_id, task_number)
        if not task:
            raise ValueError(f"Task {task_number} not found in project {project_id}")
        return task

    def list_tasks_by_project(self, project_id: int) -> List:
        """Retrieve all tasks for a specific project."""
        if not self.project_repo.get(project_id):
            raise ValueError("Project does not exist")
        return self.task_repo.list_by_project(project_id)

    def update_task(self, task_id: int, **updates):
        """Update task with any valid fields."""
        valid_fields = {"title", "description", "status", "deadline"}
        provided_fields = set(updates.keys())

        if not provided_fields:
            raise ValueError("No update data provided")

        invalid_fields = provided_fields - valid_fields
        if invalid_fields:
            raise ValueError(f"Invalid fields: {', '.join(invalid_fields)}")

        # Special handling for status -> closed_at
        if "status" in updates and updates["status"] == Status.done:
            updates["closed_at"] = datetime.utcnow()

        self.task_repo.update(task_id, updates)

    def update_task_by_number(self, project_id: int, task_number: int, **updates):
        """Update task by project ID and task number."""
        task = self.get_task_by_number(project_id, task_number)
        self.update_task(task.id, **updates)

    def delete_task(self, task_id: int):
        """Delete a task."""
        self.task_repo.delete(task_id)

    def delete_task_by_number(self, project_id: int, task_number: int):
        """Delete task by project ID and task number."""
        task = self.get_task_by_number(project_id, task_number)
        self.delete_task(task.id)

    def update_status(self, task_id: int, status: Status):
        """Update task status (for backward compatibility)."""
        self.update_task(task_id, status=status)

    def create_task_by_project_number(self, title: str, project_number: int, deadline=None):
        """Create a task using project sequential number."""
        project = self.project_repo.get_by_number(project_number)
        if not project:
            raise ValueError(f"Project #{project_number} not found")

        return self.create_task(title, project.id, deadline)

    # NEW: List tasks by project number
    def list_tasks_by_project_number(self, project_number: int):
        """List tasks using project sequential number."""
        project = self.project_repo.get_by_number(project_number)
        if not project:
            raise ValueError(f"Project #{project_number} not found")

        return self.list_tasks_by_project(project.id)

    # NEW: Get task by project number + task number
    def get_task_by_numbers(self, project_number: int, task_number: int):
        """Get task by project sequential number and task number."""
        project = self.project_repo.get_by_number(project_number)
        if not project:
            raise ValueError(f"Project #{project_number} not found")

        return self.get_task_by_number(project.id, task_number)

    def update_task_by_numbers(self, project_number: int, task_number: int, **updates):
        """Update task by project sequential number and task number."""
        task = self.get_task_by_numbers(project_number, task_number)
        self.update_task(task.id, **updates)

    # NEW: Delete task by project number + task number
    def delete_task_by_numbers(self, project_number: int, task_number: int):
        """Delete task by project sequential number and task number."""
        task = self.get_task_by_numbers(project_number, task_number)
        self.delete_task(task.id)