from fastapi import APIRouter, HTTPException
from typing import List
from models.schemas import ClienteCreate, ClienteOut
from services import cliente_service

router = APIRouter()

@router.get("/", response_model=List[dict])
async def list_clientes():
    return cliente_service.list_clientes()

@router.get("/{cliente_id}", response_model=dict)
async def get_cliente(cliente_id: int):
    c = cliente_service.get_cliente(cliente_id)
    if not c:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return c

@router.post("/", status_code=201)
async def create_cliente(payload: ClienteCreate):
    cliente_service.insert_cliente(payload.rut, payload.nombre, payload.apellido, payload.correo, payload.celular)
    return {"ok": True}

@router.put("/{cliente_id}")
async def update_cliente(cliente_id: int, payload: ClienteCreate):
    cliente_service.update_cliente(cliente_id, payload.rut, payload.nombre, payload.apellido, payload.correo, payload.celular)
    return {"ok": True}

@router.delete("/{cliente_id}")
async def delete_cliente(cliente_id: int):
    cliente_service.delete_cliente(cliente_id)
    return {"ok": True}
