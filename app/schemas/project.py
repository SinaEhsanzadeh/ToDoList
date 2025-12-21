import dotenv
from pydantic import BaseModel, Field
from typing import Optional
import os



class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Project name")
    description: Optional[str] = Field(None, max_length=500, description="Project description")


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Project name")
    description: Optional[str] = Field(None, max_length=500, description="Project description")


class ProjectRead(BaseModel):
    id: int
    project_number: int = Field(..., description="Sequential project number (displayed to users)")
    name: str
    description: Optional[str]

    class Config:
        from_attributes = True