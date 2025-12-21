from app.db.session import SessionLocal
from app.repositories.sqlalchemy import SQLTaskRepo, SQLProjectRepo
from app.services.task_service import TaskService
from app.services.project_service import ProjectService

def main():
    db = SessionLocal()

    project_repo = SQLProjectRepo(db)
    task_repo = SQLTaskRepo(db)

    project_service = ProjectService(project_repo)
    task_service = TaskService(task_repo, project_repo)

    project_id = project_service.create_project("Demo project")

    task_id = task_service.create_task(
        title="My first task",
        project_id=project_id
    )

    print("Task created:", task_id)
    print("Tasks:", task_service.list_tasks(project_id))

if __name__ == "__main__":
    main()