from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.task_schema import TaskCreate, TaskUpdate, TaskResponse
from services.task_service import TaskService
from repositories.task_repository import TaskRepository
from db.db import get_db
from typing import List

router = APIRouter()


# Dependência para instanciar o serviço com o repositório
def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    return TaskService(TaskRepository(db))


# Rota para obter todas as tarefas
@router.get("/", response_model=List[TaskResponse])
def get_tasks(task_service: TaskService = Depends(get_task_service)):
    return task_service.get_all_tasks()

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    task_service: TaskService = Depends(get_task_service)
):
    return task_service.get_task_by_id(task_id)

# Rota para criar uma nova tarefa
@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(
    task_data: TaskCreate,
    task_service: TaskService = Depends(get_task_service),
):
    return task_service.create_task(task_data)


# Rota para atualizar uma tarefa
@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    task_service: TaskService = Depends(get_task_service),
):
    task = task_service.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    updated_task = task_service.update_task(task_id, task_data)
    return updated_task


# Rota para deletar uma tarefa
@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    task_service: TaskService = Depends(get_task_service),
):
    task = task_service.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task_service.delete_task(task_id)
    return {"message": "Task deleted"}
