from fastapi import FastAPI
from app.routers import usuario

app = FastAPI()

app.include_router(usuario.router)
