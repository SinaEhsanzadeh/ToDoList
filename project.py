from __future__ import annotations

import textwrap
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
import uuid
import config

class ProjectValidationError(ValueError):
    pass

class ProjectNameRequiredError(ProjectValidationError):
    pass

class ProjectNameTooLongError(ProjectValidationError):
    pass

class ProjectDescriptionTooLongError(ProjectValidationError):
    pass

def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def _parse_iso_to_datetime(iso_str: str) -> Optional[datetime]:
    if not iso_str:
        return None

    s = iso_str

    try:
        if s.endswith("Z"):
            s = s[:-1] + "+00:00"

        dt = datetime.fromisoformat(s)

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return None

def _format_created_at(iso_str: str) -> str:
    dt = _parse_iso_to_datetime(iso_str)

    if not dt:
        return iso_str or "(unknown)"

    dt_utc = dt.astimezone(timezone.utc)

    return dt_utc.strftime("%b %d, %Y %H:%M:%S UTC")

class Project:
    name: str
    description: Optional[str]
    tasks: List["Task"]
    created_at: str
    id: str

    def __init__(self, name: str, description: Optional[str] = "") -> None:
        if name is None:
            name = ""

        name = name.strip()
        if description is None:
            description = ""

        if not name:
            raise ProjectNameRequiredError("Project name is required and cannot be empty.")

        if len(name) > config.PROJECT_MAX_NAME_LEN:
            raise ProjectNameTooLongError(f"Project name must be at most {config.PROJECT_MAX_NAME_LEN} characters.")

        if len(description) > config.PROJECT_MAX_DESCRIPTION_LEN:
            raise ProjectDescriptionTooLongError(f"Project description must be at most {config.PROJECT_MAX_DESCRIPTION_LEN} characters.")

        self.name = name
        self.description = description
        self.tasks = []
        self.created_at = _now_iso()
        self.id = str(uuid.uuid4())

    def view(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "task_count": len(self.tasks),
            "tasks": [getattr(t, "id", None) for t in self.tasks],
        }

    def pretty(self, width: int = 72) -> str:
        header = f"Project: {self.name}  (id: {self.id})"
        created = f"Created: {_format_created_at(self.created_at)}"
        task_count = f"Tasks: {len(self.tasks)}"

        desc = self.description or "(none)"
        wrapped_desc = textwrap.fill(desc, width=width, subsequent_indent="  ")

        lines = [
            "-" * 60,
            header,
            created,
            f"Description:\n  {wrapped_desc}",
            task_count,
        ]

        if self.tasks:
            lines.append("")
            lines.append("Task list:")
            for i, t in enumerate(self.tasks, start=1):
                t_name = getattr(t, "name", "<no-name>")
                t_id = getattr(t, "id", "<no-id>")

                t_state = getattr(t, "state", None)
                state_part = f"[{t_state}]" if t_state is not None else ""
                lines.append(f"  {i}. {state_part} {t_name} (id={t_id})".rstrip())
        lines.append("-" * 60)
        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "tasks": [t.to_dict() if hasattr(t, "to_dict") else asdict(t) for t in self.tasks],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any], task_factory: Optional[callable] = None) -> "Project":
        proj = cls(
            name=data["name"],
            description=data.get("description", ""),
            created_at=data.get("created_at", _now_iso()),
            id=data.get("id", str(uuid.uuid4())),
        )
        raw_tasks = data.get("tasks", [])
        if task_factory:
            proj.tasks = [task_factory(t) for t in raw_tasks]
        else:
            proj.tasks = raw_tasks
        return proj

    def __repr__(self) -> str:
        return f"<Project {self.name!r} id={self.id} tasks={len(self.tasks)}>"

