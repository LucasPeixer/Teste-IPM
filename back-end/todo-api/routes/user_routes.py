from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dtos import UserCreateDTO, UserUpdateDTO, UserResponseDTO
from usecases import UserUseCase
from repository import UserRepository
from db import get_db

router = APIRouter()

# Iniciando o repositório e o use case
user_repository = UserRepository()
user_use_case = UserUseCase(user_repository)

@router.get("/", response_model=List[UserResponseDTO])
def get_users(db: Session = Depends(get_db)):
    return user_use_case.get_all_users(db)

@router.get("/{user_id}", response_model=UserResponseDTO)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_use_case.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=UserResponseDTO)
def create_user(user_data: UserCreateDTO, db: Session = Depends(get_db)):
    return user_use_case.create_user(db, user_data)

@router.put("/{user_id}", response_model=UserResponseDTO)
def update_user(user_id: int, user_data: UserUpdateDTO, db: Session = Depends(get_db)):
    updated_user = user_use_case.update_user(db, user_id, user_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}", response_model=bool)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    result = user_use_case.delete_user(db, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result
