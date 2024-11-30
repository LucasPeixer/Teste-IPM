from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreateDTO(BaseModel):
    username: str
    email: str
    password: str

class UserResponseDTO(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True
