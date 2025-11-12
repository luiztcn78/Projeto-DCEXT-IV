from fastapi import FastAPI, Depends
from sqlalchemy import text
from app.database import get_db, engine, Base
from app.models import usuario, diario, emocao, atividade, lembrete

# Import routers
from app.routers import usuario as usuario_router
from app.routers import diario as diario_router
from app.routers import lembrete as lembrete_router

app = FastAPI(title="Sistema DCEXT-IV", version="1.0.0")

# Incluir routers
app.include_router(usuario_router.router)
app.include_router(diario_router.router)
app.include_router(lembrete_router.router)

@app.on_event("startup")
async def startup_event():
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")

@app.get("/")
def root():
    return {"message": "Sistema DCEXT-IV API está rodando!"}

@app.get("/health")
def health_check(db = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}