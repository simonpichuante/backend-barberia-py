from fastapi import APIRouter, Depends, HTTPException
from core.auth import get_current_user
from services.historial_service import HistorialService
from config import db
from exceptions.custom_exceptions import NotFoundError

router = APIRouter(prefix="/historial", tags=["historial"])
service = HistorialService(db)

@router.get("/")
def list_historial(_=Depends(get_current_user)):
    return service.list()

@router.post("/")
def create_historial(body: dict, _=Depends(get_current_user)):
    return service.create(body)

@router.get("/{id}")
def get_historial(id: int, _=Depends(get_current_user)):
    try:
        return service.get(id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{id}")
def delete_historial(id: int, _=Depends(get_current_user)):
    return service.delete(id)
