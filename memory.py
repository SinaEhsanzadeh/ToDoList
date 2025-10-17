from typing import List, Optional
from project import Project


class MemoryStore:
    def __init__(self) -> None:
        self._projects: List[Project] = []

    def add_project(self, project: Project) -> None:
        self._projects.append(project)

    def list_projects(self) -> List[Project]:
        return list(self._projects)  # return a shallow copy

    def get_project(self, project_id: str) -> Optional[Project]:
        for p in self._projects:
            if p.id == project_id:
                return p
        return None

    def remove_project(self, project_id: str) -> bool:
        for i, p in enumerate(self._projects):
            if p.id == project_id:
                del self._projects[i]
                return True
        return False
