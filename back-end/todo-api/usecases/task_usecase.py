from sqlalchemy.orm import Session
from models.task_model import Task
from repository import TaskRepository
from dtos import TaskCreateDTO, TaskUpdateDTO
from typing import List, Optional

class TaskUseCase:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def get_all_tasks(self, db: Session) -> List[Task]:
        return self.task_repository.get_all(db)

    def create_task(self, db: Session, task_data: TaskCreateDTO) -> Task:
        self._validate_task_status(task_data.status)
        new_task = Task(
            title=task_data.title,
            description=task_data.description,
            status=task_data.status,
            expired_at=task_data.expired_at
        )
        return self.task_repository.create(db, new_task)

    def update_task(self, db: Session, task_id: int, task_data: TaskUpdateDTO) -> Optional[Task]:
        task = self.task_repository.get_by_id(db, task_id)
        if not task:
            return None
        if task_data.title:
            task.title = task_data.title
        if task_data.description:
            task.description = task_data.description
        if task_data.status:
            self._validate_task_status(task_data.status)
            task.status = task_data.status
        if task_data.expired_at:
            task.expired_at = task_data.expired_at
        return self.task_repository.update(db, task)

    def delete_task(self, db: Session, task_id: int) -> bool:
        task = self.task_repository.get_by_id(db, task_id)
        if not task:
            return False
        self.task_repository.delete(db, task)
        return True

    def _validate_task_status(self, status: str) -> None:
        valid_statuses = {"Em andamento", "Finalizado"}
        if status not in valid_statuses:
            raise ValueError(f"Status inválido! Use um dos seguintes: {', '.join(valid_statuses)}")
