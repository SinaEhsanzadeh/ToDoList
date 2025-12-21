from sqlalchemy.orm import Session
from app.models.project import Project
from app.models.task import Task

class SQLProjectRepo:
    def __init__(self, db: Session):
        self.db = db

    def add(self, data):
        last_project = self.db.query(Project).order_by(Project.project_number.desc()).first()
        next_number = 1
        if last_project:
            next_number = last_project.project_number + 1

        data["project_number"] = next_number
        project = Project(**data)
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project.id

    def get(self, project_id):
        return self.db.get(Project, project_id)

    def delete(self, project_id):
        project = self.get(project_id)
        if project:
            deleted_number = project.project_number

            # Delete the project (cascade will delete tasks)
            self.db.delete(project)
            self.db.commit()

            # Renumber ALL remaining projects to fill gaps
            # Get all projects ordered by current project_number
            all_projects = self.db.query(Project).order_by(Project.project_number).all()

            # Renumber sequentially starting from 1
            for i, p in enumerate(all_projects, start=1):
                if p.project_number != i:
                    p.project_number = i

            self.db.commit()

    def list_all(self):
        """List all projects."""
        return self.db.query(Project).order_by(Project.id).all()

    def update(self, project_id: int, data: dict):
        """Update project fields."""
        project = self.get(project_id)
        if project:
            for key, value in data.items():
                setattr(project, key, value)
            self.db.commit()

    def get_by_number(self, project_number: int):
        """Get project by its sequential number."""
        return self.db.query(Project).filter(Project.project_number == project_number).first()

    def list_all_by_number(self):
        """List all projects ordered by sequential number."""
        return self.db.query(Project).order_by(Project.project_number).all()


class SQLTaskRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_by_number(self, project_id: int, task_number: int):
        """Get task by project ID and task number."""
        return self.db.query(Task).filter(
            Task.project_id == project_id,
            Task.task_number == task_number
        ).first()

    def add(self, data):
        last_task = self.db.query(Task).filter(
            Task.project_id == data["project_id"]
        ).order_by(Task.task_number.desc()).first()

        next_task_number = 1
        if last_task:
            next_task_number = last_task.task_number + 1

        data["task_number"] = next_task_number
        task = Task(**data)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task.id

    def get(self, task_id):
        return self.db.get(Task, task_id)

    def list_by_project(self, project_id):
        return self.db.query(Task).filter(Task.project_id == project_id).all()

    def update(self, task_id, data):
        task = self.get(task_id)
        for k, v in data.items():
            setattr(task, k, v)
        self.db.commit()

    def delete(self, task_id):
        task = self.get(task_id)
        if task:
            project_id = task.project_id
            task_number = task.task_number

            # Delete the task
            self.db.delete(task)
            self.db.commit()

            # Renumber remaining tasks in the same project
            remaining_tasks = self.db.query(Task).filter(
                Task.project_id == project_id,
                Task.task_number > task_number
            ).order_by(Task.task_number).all()

            for i, t in enumerate(remaining_tasks, start=task_number):
                t.task_number = i

            self.db.commit()
