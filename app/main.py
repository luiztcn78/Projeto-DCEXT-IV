from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends
from sqlalchemy import text
from app.database import get_db, engine, Base
from app.models import usuario, diario, emocao, atividade, lembrete, compartilhamento

# Import routers
from app.routers import usuario as usuario_router
from app.routers import diario as diario_router
from app.routers import lembrete as lembrete_router
from app.routers import atividade as atividade_router
from app.routers import emocao as emocao_router
from app.routers import compartilhamento as compartilhamento_router

app = FastAPI(
    title="Sistema DCEXT-IV API",
    description="""
    Sistema de gerenciamento para idosos e familiares com compartilhamento de dados controlado.
    
    ## Funcionalidades
    
    ### Para Idosos:
    * Gerenciar diários, emoções, atividades e lembretes
    * Controlar quais familiares podem acessar seus dados
    * Conceder/revogar permissões específicas
    
    ### Para Familiares:
    * Acessar dados compartilhados pelos idosos
    * Visualizar informações apenas com permissão explícita
    
    ## Autenticação
    * O sistema usa autenticação básica por email/senha
    * Cada usuário deve fazer login para acessar seus endpoints
    """,
    version="2.0.0",
    contact={
        "name": "Suporte DCEXT-IV",
        "email": "suporte@dcext-iv.com",
    },
    license_info={
        "name": "MIT",
    }
)

# Incluir routers
app.include_router(usuario_router.router)
app.include_router(diario_router.router)
app.include_router(lembrete_router.router)
app.include_router(atividade_router.router)
app.include_router(emocao_router.router)
app.include_router(compartilhamento_router.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")

@app.get("/")
def root():
    return {"message": "Sistema DCEXT-IV API está rodando! Acesse /docs para ver a documentação Swagger."}

@app.get("/health")
def health_check(db = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}