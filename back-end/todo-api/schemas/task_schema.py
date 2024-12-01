from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TaskBase(BaseModel):
    title: str
    description: str
    dueDate: Optional[datetime] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    status: Optional[str] = None
    dueDate: Optional[datetime] = None

class TaskResponse(TaskBase):
    id: int
    status: str

    class Config:
        from_attributes = True
