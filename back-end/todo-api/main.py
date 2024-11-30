from fastapi import FastAPI
from routes import register_routes

# Cria a aplicação FastAPI
app = FastAPI(
    title="To-Do API",
    description="API para gerenciar tarefas e usuários",
    version="1.0.0"
)

# Registra as rotas
register_routes(app)
