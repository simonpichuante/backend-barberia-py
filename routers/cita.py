from fastapi import APIRouter, HTTPException
from typing import List
from models.schemas import CitaCreate, CitaOut
from services import cita_service

router = APIRouter()

@router.get("/", response_model=List[dict])
async def list_citas():
    return cita_service.list_citas()

@router.get("/{cita_id}", response_model=dict)
async def get_cita(cita_id: int):
    c = cita_service.get_cita(cita_id)
    if not c:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return c

@router.post("/", status_code=201)
async def create_cita(payload: CitaCreate):
    cita_service.insert_cita(payload.id_solicitud, payload.id_cliente, payload.id_servicio, payload.id_barbero, payload.fecha_programada, payload.observaciones)
    return {"ok": True}

@router.delete("/{cita_id}")
async def delete_cita(cita_id: int):
    cita_service.delete_cita(cita_id)
    return {"ok": True}

# Gestores endpoints
@router.post("/convertir-solicitud/{id_solicitud}")
async def convertir_solicitud(id_solicitud: int, id_hora_disponible: int):
    cita_service.convertir_solicitud_a_cita(id_solicitud, id_hora_disponible)
    return {"ok": True}

@router.post("/asignar-barbero/{id_cita}")
async def asignar_barbero(id_cita: int):
    cita_service.asignar_barbero_automatico(id_cita)
    return {"ok": True}

@router.post("/finalizar/{id_cita}")
async def finalizar(id_cita: int, motivo: str = ""):
    cita_service.finalizar_cita(id_cita, motivo)
    return {"ok": True}

@router.post("/cancelar/{id_cita}")
async def cancelar(id_cita: int, motivo: str = ""):
    cita_service.cancelar_cita(id_cita, motivo)
    return {"ok": True}

@router.post("/reprogramar/{id_cita}")
async def reprogramar(id_cita: int, nueva_fecha: str, id_hora_nueva: int):
    # nueva_fecha puede recibirse en ISO e internamente oracledb aceptará datetime python
    from datetime import datetime
    fecha = datetime.fromisoformat(nueva_fecha)
    cita_service.reprogramar_cita(id_cita, fecha, id_hora_nueva)
    return {"ok": True}
