from datetime import datetime
from app.db.session import SessionLocal
from app.models.task import Task, Status

def run():
    db = SessionLocal()
    now = datetime.utcnow()

    tasks = db.query(Task).filter(
        Task.status != Status.done,
        Task.deadline < now
    ).all()

    for t in tasks:
        t.status = Status.done
        t.closed_at = now

    db.commit()
