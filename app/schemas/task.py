from datetime import datetime
from pydantic import BaseModel, Field, validator
from typing import Optional, Any, Union
from app.models.task import Status


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Task title")
    description: Optional[str] = Field(None, max_length=500, description="Task description")
    deadline: Optional[Union[datetime, str]] = Field(
        None,
        description="Deadline in formats: '2023-12-31', '2023-12-31 23:59', '2023-12-31T23:59:00', or natural language like 'tomorrow 2pm'"
    )

    @validator('deadline', pre=True)
    def parse_deadline(cls, value: Any) -> Optional[datetime]:
        """Parse deadline from string or return datetime object."""
        if value is None:
            return None

        if isinstance(value, datetime):
            return value

        if not isinstance(value, str):
            raise ValueError("Deadline must be a string or datetime")

        value = value.strip()
        if not value:
            return None

        try:
            return datetime.fromisoformat(value.replace('Z', '+00:00'))
        except ValueError:
            pass

        date_formats = [
            "%Y-%m-%d %H:%M",  # 2023-12-31 23:59
            "%Y-%m-%dT%H:%M:%S",  # 2023-12-31T23:59:00
            "%Y-%m-%d",  # 2023-12-31
            "%d/%m/%Y %H:%M",  # 31/12/2023 23:59
            "%d/%m/%Y",  # 31/12/2023
            "%m/%d/%Y %H:%M",  # 12/31/2023 23:59
            "%m/%d/%Y",  # 12/31/2023
        ]

        for fmt in date_formats:
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue

        try:
            import dateparser
            parsed = dateparser.parse(
                value,
                settings={'PREFER_DATES_FROM': 'future', 'RETURN_AS_TIMEZONE_AWARE': False}
            )
            if parsed:
                return parsed
        except ImportError:
            pass
        except Exception:
            pass

        raise ValueError(
            f"Could not parse deadline: '{value}'. "
            f"Use formats like '2023-12-31', '2023-12-31 14:30', or '2023-12-31T14:30:00'"
        )

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100, description="Task title")
    description: Optional[str] = Field(None, max_length=500, description="Task description")
    status: Optional[Status] = Field(None, description="Task status")
    deadline: Optional[Union[datetime, str]] = Field(
        None,
        description="Deadline in formats: '2023-12-31', '2023-12-31 23:59', or '2023-12-31T23:59:00'"
    )

    @validator('deadline', pre=True)
    def parse_deadline(cls, value: Any) -> Optional[datetime]:
        return TaskCreate.parse_deadline.__func__(cls, value)


class TaskRead(BaseModel):
    id: int
    project_id: int
    task_number: int
    title: str
    description: Optional[str]
    status: Status
    deadline: Optional[datetime]
    closed_at: Optional[datetime]

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }