from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dtos import TaskCreateDTO, TaskUpdateDTO, TaskResponseDTO
from usecases import TaskUseCase
from repository import TaskRepository
from db import get_db

router = APIRouter()

# Iniciando o repositório e o use case
task_repository = TaskRepository()
task_use_case = TaskUseCase(task_repository)

@router.get("/", response_model=List[TaskResponseDTO])
def get_tasks(db: Session = Depends(get_db)):
    tasks = task_use_case.get_all_tasks(db)
    # Convertendo o modelo Task para TaskResponseDTO
    return [TaskResponseDTO.from_orm(task) for task in tasks]

@router.post("/", response_model=TaskResponseDTO)
def create_task(task_data: TaskCreateDTO, db: Session = Depends(get_db)):
    created_task = task_use_case.create_task(db, task_data)
    # Convertendo o modelo Task para TaskResponseDTO
    return TaskResponseDTO.from_orm(created_task)

@router.put("/{task_id}", response_model=TaskResponseDTO)
def update_task(task_id: int, task_data: TaskUpdateDTO, db: Session = Depends(get_db)):
    updated_task = task_use_case.update_task(db, task_id, task_data)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    # Convertendo o modelo Task para TaskResponseDTO
    return TaskResponseDTO.from_orm(updated_task)

@router.delete("/{task_id}", response_model=bool)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    result = task_use_case.delete_task(db, task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return result
