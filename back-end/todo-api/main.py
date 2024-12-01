# main.py
from fastapi import FastAPI
from middleware.cors import add_cors_middleware
from routes.task_routes import router as task_router

app = FastAPI()

add_cors_middleware(app)

# Incluir rotas de tasks
app.include_router(task_router, prefix="/api/v1/tasks")
