from sqlalchemy.orm import Session
from models.task_model import Task

class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Task).all()

    def get_by_id(self, task_id: int):
        return self.db.query(Task).filter(Task.id == task_id).first()

    def create(self, task_data):
        new_task = Task(**task_data.dict())
        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)
        return new_task

    def update(self, task: Task):
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task: Task):
        self.db.delete(task)
        self.db.commit()

