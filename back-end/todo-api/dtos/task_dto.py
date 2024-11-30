from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TaskCreateDTO(BaseModel):
    title: str
    description: Optional[str] = None
    status: str
    expired_at: Optional[datetime] = None

class TaskUpdateDTO(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    expired_at: Optional[datetime] = None

class TaskResponseDTO(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: str
    created_at: datetime
    expired_at: Optional[datetime] = None

    class Config:
        orm_mode = True
