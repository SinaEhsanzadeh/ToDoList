from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Optional, Dict, Any
import uuid
import textwrap

from config import TASK_MAX_NAME_LEN, TASK_MAX_DESCRIPTION_LEN

class TaskValidationError(ValueError):
    pass

class TaskNameRequiredError(TaskValidationError):
    pass

class TaskNameTooLongError(TaskValidationError):
    pass

class TaskDescriptionTooLongError(TaskValidationError):
    pass

class InvalidTaskStateError(TaskValidationError):
    pass

class TaskState(str, Enum):
    TODO = "TODO"
    DOING = "DOING"
    DONE = "DONE"

    @classmethod
    def from_str(cls, s: str) -> "TaskState":
        s = s.strip().upper()
        for state in cls:
            if state.value == s:
                return state
        raise InvalidTaskStateError(f"Invalid state '{s}'. Valid: TODO, DOING, DONE.")

def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def _format_created_at(iso_str: str) -> str:
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return dt.strftime("%b %d, %Y %H:%M:%S UTC")
    except Exception:
        return iso_str or "(unknown)"

@dataclass(init=False)
class Task:
    name: str
    description: Optional[str]
    state: TaskState
    created_at: str
    id: str

    def __init__(self, name: str, description: Optional[str] = "") -> None:
        if name is None:
            name = ""

        name = name.strip()
        if description is None:
            description = ""

        if not name:
            raise TaskNameRequiredError("Task name cannot be empty.")

        if len(name) > TASK_MAX_NAME_LEN:
            raise TaskNameTooLongError(f"Task name must be at most {TASK_MAX_NAME_LEN} characters.")

        if len(description) > TASK_MAX_DESCRIPTION_LEN:
            raise TaskDescriptionTooLongError(f"Task description must be at most {TASK_MAX_DESCRIPTION_LEN} characters.")

        self.name = name
        self.description = description
        self.state = TaskState.TODO
        self.created_at = _now_iso()
        self.id = str(uuid.uuid4())

    def set_state(self, new_state: str | TaskState) -> None:
        if isinstance(new_state, str):
            self.state = TaskState.from_str(new_state)

        elif isinstance(new_state, TaskState):
            self.state = new_state

        else:
            raise InvalidTaskStateError(f"Invalid type for state: {type(new_state)}")

    def view(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "state": self.state.value,
            "created_at": self.created_at,
        }

    def pretty(self, width: int = 72) -> str:
        desc = self.description or "(none)"
        wrapped_desc = textwrap.fill(desc, width=width, subsequent_indent="  ")
        return (
            f"{'-'*50}\n"
            f"Task: {self.name}  (id: {self.id})\n"
            f"State: {self.state.value}\n"
            f"Created: {_format_created_at(self.created_at)}\n"
            f"Description:\n  {wrapped_desc}\n"
            f"{'-'*50}"
        )

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["state"] = self.state.value
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        task = cls(
            name=data["name"],
            description=data.get("description", ""),
        )
        task.state = TaskState.from_str(data.get("state", TaskState.TODO.value))
        task.id = data.get("id", task.id)
        task.created_at = data.get("created_at", task.created_at)
        return task

    def __repr__(self) -> str:
        return f"<Task {self.name!r} state={self.state.value} id={self.id}>"