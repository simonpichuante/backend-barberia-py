from fastapi import APIRouter, Depends, HTTPException
from core.auth import get_current_user
from services.solicitud_service import SolicitudService
from config import db
from exceptions.custom_exceptions import NotFoundError

router = APIRouter(prefix="/solicitudes", tags=["solicitudes"])
service = SolicitudService(db)

@router.get("/")
def list_solicitudes(_=Depends(get_current_user)):
    return service.list()

@router.post("/")
def create_solicitud(body: dict):
    # permitir creación pública para clientes (sin token) también es posible
    return service.create(body)

@router.get("/{id}")
def get_solicitud(id: int, _=Depends(get_current_user)):
    try:
        return service.get(id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{id}")
def delete_solicitud(id: int, _=Depends(get_current_user)):
    return service.delete(id)
