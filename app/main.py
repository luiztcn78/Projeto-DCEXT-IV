from fastapi import FastAPI
#from app.routers import usuario

app = FastAPI()

#app.include_router(usuario.router)

#rota teste
@app.get("/")
def root():
    return {"testando": "Rodou"}
