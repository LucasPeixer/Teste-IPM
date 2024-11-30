from sqlalchemy import DateTime,Enum,Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class TaskStatusEnum(enum.Enum):
    in_progress = "Em andamento"
    completed = "Finalizado"

class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(String)
    status = Column(Enum(TaskStatusEnum), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    expired_at = Column(DateTime)