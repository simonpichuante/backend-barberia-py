# app.py (versión con Lifespan)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import os
from dotenv import load_dotenv


load_dotenv()

# importa init_pool desde tu db.py (asegúrate de que db.py esté en la misma carpeta)
from db import init_pool

logger = logging.getLogger("barberia")
logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan handler: se ejecuta en startup (antes del yield)
    y en shutdown (después del yield).
    """
    try:
        # Inicializa pool de forma síncrona (init_pool es síncrono en db.py)
        # Si tu init_pool fuera async, await init_pool()
        init_pool(min=1, max=6, increment=1)
        logger.info("Pool Oracle inicializado en lifespan (startup).")
    except Exception as e:
        logger.exception("No se pudo inicializar pool Oracle en startup: %s", e)
        # no lanzamos para que la app arranque; decide si quieres fallar en producción
    yield
    # shutdown: aquí puedes cerrar recursos si quieres (si db.py ofrece close)
    logger.info("Lifespan shutdown complete.")

app = FastAPI(title="Barberia - API (FastAPI)", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en producción restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# importa routers después de crear app para evitar import cycles
from routers import cliente, cita  # tu código existente
app.include_router(cliente.router, prefix="/api/clientes", tags=["clientes"])
app.include_router(cita.router, prefix="/api/citas", tags=["citas"])

@app.get("/health")
async def health():
    return {"status": "ok"}

# Permite ejecutar con `python app.py` si prefieres
if __name__ == "__main__":
    import uvicorn
    # usa reload=True sólo en desarrollo
    uvicorn.run("app:app", host="127.0.0.1", port=3000, reload=True)
