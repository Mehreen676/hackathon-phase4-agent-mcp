from pydantic import BaseModel
from typing import Optional


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = ""


class TaskRead(BaseModel):
    id: int
    user_id: str
    title: str
    description: Optional[str] = ""
    completed: bool
