from repositories.task_repository import TaskRepository
from sqlalchemy.orm import Session
from models.task_model import Task

class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def get_all_tasks(self):
        return self.repository.get_all()

    def get_task_by_id(self, task_id: int):
        return self.repository.get_by_id(task_id)

    def create_task(self, task_data):
        return self.repository.create(task_data)

    def update_task(self, task_id: int, task_data):
        task = self.get_task_by_id(task_id)
        for key, value in task_data.dict(exclude_unset=True).items():
            setattr(task, key, value)
        return self.repository.update(task)

    def delete_task(self, task_id: int):
        task = self.get_task_by_id(task_id)
        self.repository.delete(task)

