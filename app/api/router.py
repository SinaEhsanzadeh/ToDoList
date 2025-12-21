from fastapi import APIRouter
from app.api.projects import router as projects_router
from app.api.tasks import router as tasks_router

api_router = APIRouter()
api_router.include_router(projects_router)
api_router.include_router(tasks_router)