from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from pydantic import ValidationError
from db import get_db
from models import Task
from repository import TaskRepository
from usecases import TaskUseCase
from dtos import TaskCreateDTO, TaskUpdateDTO, TaskResponseDTO

router = APIRouter()

task_repository = TaskRepository()
task_usecase = TaskUseCase(task_repository)

# 1. Listar todas as tarefas
@router.get("/tasks", response_model=list[TaskResponseDTO])
def get_tasks(db: Session = Depends(get_db)):
    tasks = task_usecase.get_all_tasks(db)
    return tasks

# 2. Adicionar uma nova tarefa
@router.post("/tasks", response_model=TaskResponseDTO, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreateDTO, db: Session = Depends(get_db)):
    try:
        new_task = task_usecase.create_task(db, task)
        return new_task
    except ValidationError as ve:
        raise HTTPException(status_code=400, detail="Invalid data format", headers={"Validation-Error": str(ve)})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# 3. Editar o conteúdo de uma tarefa
@router.put("/tasks/{task_id}", response_model=TaskResponseDTO)
def update_task(task_id: int, task: TaskUpdateDTO, db: Session = Depends(get_db)):
    updated_task = task_usecase.update_task(db, task_id, task)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

# 4. Marcar tarefa como concluída
@router.patch("/tasks/{task_id}/complete", response_model=TaskResponseDTO)
def mark_task_as_completed(task_id: int, db: Session = Depends(get_db)):
    task = task_usecase.mark_as_completed(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# 5. Deletar uma tarefa
@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    result = task_usecase.delete_task(db, task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted successfully"}
