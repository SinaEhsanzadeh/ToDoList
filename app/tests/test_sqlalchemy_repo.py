from app.db.session import SessionLocal
from app.repositories.sqlalchemy import SQLProjectRepo, SQLTaskRepo

def test_project_task_flow():
    db = SessionLocal()
    project_repo = SQLProjectRepo(db)
    task_repo = SQLTaskRepo(db)

    pid = project_repo.add({"name": "Integration"})
    tid = task_repo.add({"title": "DB task", "project_id": pid})

    task = task_repo.get(tid)
    assert task.title == "DB task"
