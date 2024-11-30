from fastapi import FastAPI
from .task_routes import router as task_router
from .user_routes import router as user_router

def register_routes(app: FastAPI):
    app.include_router(task_router, prefix="/api/v1/tasks")
    app.include_router(user_router, prefix="/api/v1/users")
