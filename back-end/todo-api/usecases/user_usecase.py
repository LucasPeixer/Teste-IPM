from sqlalchemy.orm import Session
from repository import UserRepository
from dtos import UserCreateDTO, UserUpdateDTO, UserResponseDTO
from models import User
from typing import List, Optional
from passlib.context import CryptContext

class UserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_all_users(self, db: Session) -> List[UserResponseDTO]:
        users = self.user_repository.get_all(db)
        return [UserResponseDTO.from_orm(user) for user in users]

    def get_user(self, db: Session, user_id: int) -> Optional[UserResponseDTO]:
        user = self.user_repository.get_by_id(db, user_id)
        if not user:
            return None
        return UserResponseDTO.from_orm(user)

    def create_user(self, db: Session, user_data: UserCreateDTO) -> UserResponseDTO:
        hashed_password = self.pwd_context.hash(user_data.password)
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            password=hashed_password,
            full_name=user_data.full_name
        )
        created_user = self.user_repository.create(db, new_user)
        return UserResponseDTO.from_orm(created_user)

    def update_user(self, db: Session, user_id: int, user_data: UserUpdateDTO) -> Optional[UserResponseDTO]:
        user = self.user_repository.get_by_id(db, user_id)
        if not user:
            return None
        if user_data.username:
            user.username = user_data.username
        if user_data.email:
            user.email = user_data.email
        if user_data.full_name:
            user.full_name = user_data.full_name
        updated_user = self.user_repository.update(db, user)
        return UserResponseDTO.from_orm(updated_user)

    def delete_user(self, db: Session, user_id: int) -> bool:
        user = self.user_repository.get_by_id(db, user_id)
        if not user:
            return False
        self.user_repository.delete(db, user)
        return True
