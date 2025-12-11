# routers/barberos.py
from fastapi import APIRouter, HTTPException, Depends
from core.auth import get_current_user
from config import db
from services.barbero_service import BarberoService
from exceptions.custom_exceptions import NotFoundError

router = APIRouter(prefix="/barberos")
barbero_service = BarberoService(db)

@router.get("/")
def list_barberos(current_user=Depends(get_current_user)):
    return barbero_service.list()

@router.post("/")
def create_barbero(payload: dict, current_user=Depends(get_current_user)):
    return barbero_service.create(payload)

@router.get("/{id}")
def get_barbero(id: int, current_user=Depends(get_current_user)):
    try:
        return barbero_service.get(id)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Barbero no encontrado")

@router.put("/{id}")
def update_barbero(id: int, payload: dict, current_user=Depends(get_current_user)):
    return barbero_service.update(id, payload)

@router.delete("/{id}")
def delete_barbero(id: int, current_user=Depends(get_current_user)):
    return barbero_service.delete(id)
