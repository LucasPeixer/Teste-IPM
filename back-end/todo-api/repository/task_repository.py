from sqlalchemy.orm import Session
from models.task_model import Task
from dtos.task_dto import TaskCreate, TaskUpdate

class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_tasks(self):
        return self.db.query(Task).all()

    def create_task(self, task_data: TaskCreate):
        db_task = Task(**task_data.dict())
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def update_task(self, task_id: int, task_data: TaskUpdate):
        task = self.db.query(Task).filter(Task.id == task_id).first()
        if task:
            for key, value in task_data.dict(exclude_unset=True).items():
                setattr(task, key, value)
            self.db.commit()
            self.db.refresh(task)
        return task

    def complete_task(self, task_id: int):
        task = self.db.query(Task).filter(Task.id == task_id).first()
        if task:
            task.status = "Finalizado"
            self.db.commit()
            self.db.refresh(task)
        return task

    def delete_task(self, task_id: int):
        task = self.db.query(Task).filter(Task.id == task_id).first()
        if task:
            self.db.delete(task)
            self.db.commit()
        return task
