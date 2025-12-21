from fastapi import FastAPI
from app.api.router import api_router

app = FastAPI(
    title="ToDo List API",
    description="""
    # Project & Task Management API

    ## Key Concepts:

    ### Project Numbering
    - Projects have two identifiers:
      1. **Internal ID** (`id`): Database primary key, never changes
      2. **Display Number** (`project_number`): Sequential number shown to users

    ### Important:
    - **ALWAYS use `project_number` in API URLs**
    - `project_number` is sequential (1, 2, 3...) and renumbers when projects are deleted
    - Example: `/projects/1/tasks/2` means "task #2 in project #1"

    ### Task Numbering
    - Tasks are numbered sequentially **within each project**
    - Task #1, #2, #3 in Project #1
    - Task #1, #2, #3 in Project #2 (separate numbering)

    ## API Usage Example:
    1. `POST /projects/` → Creates project #1
    2. `POST /projects/1/tasks/` → Creates task #1 in project #1
    3. `GET /projects/1/tasks/1` → Gets task #1 in project #1
    """,
    version="1.0.0",
    contact={
        "name": "ToDo List API Support",
        "email": "support@example.com",
    },
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(api_router)


@app.get("/", include_in_schema=False)
def root():
    return {
        "message": "ToDo List API",
        "docs": "/docs",
        "note": "Projects are accessed by project_number, not internal ID"
    }