import os
from fastapi import Request, HTTPException
from fastapi.middleware.base import BaseHTTPMiddleware
from jose import jwt, JWTError
from starlette.status import HTTP_401_UNAUTHORIZED
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Verificar rota pública
        if request.url.path in ["/auth/login", "/auth/create-account"]:
            return await call_next(request)

        # Obter o token do cabeçalho
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="Token de autenticação ausente"
            )

        token = auth_header.split(" ")[1]
        try:
            # Decodificar o token
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            request.state.user = payload.get("sub")
        except JWTError:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="Token inválido"
            )

        return await call_next(request)
