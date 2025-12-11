import uvicorn
from fastapi import FastAPI
from config import db
from routers import auth, citas, clientes, barberos, reportes

app = FastAPI(title="Barberia API - FastAPI (Python)")

# Registrar routers
app.include_router(auth.router)
app.include_router(citas.router)
app.include_router(clientes.router)
app.include_router(barberos.router)
app.include_router(reportes.router)

@app.on_event("startup")
def startup_event():
    db.init()

@app.get("/health")
def health():
    return {"ok": True}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
