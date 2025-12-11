from fastapi import APIRouter, Depends, HTTPException
from core.auth import get_current_user
from services.cliente_service import ClienteService
from config import db
from exceptions.custom_exceptions import NotFoundError

router = APIRouter(prefix="/clientes", tags=["clientes"])
service = ClienteService(db)

@router.get("/")
def list_clientes(_=Depends(get_current_user)):
    return service.list()

@router.post("/")
def create_cliente(body: dict, _=Depends(get_current_user)):
    return service.create(body)

@router.get("/{id}")
def get_cliente(id: int, _=Depends(get_current_user)):
    try:
        return service.get(id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{id}")
def update_cliente(id: int, body: dict, _=Depends(get_current_user)):
    return service.update(id, body)

@router.delete("/{id}")
def delete_cliente(id: int, _=Depends(get_current_user)):
    return service.delete(id)
