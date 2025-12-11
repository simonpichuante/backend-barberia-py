from fastapi import APIRouter, Depends, HTTPException
from core.auth import get_current_user
from services.report_service import ReportService
from config import db

router = APIRouter(prefix="/reportes", tags=["reportes"])
service = ReportService(db)

@router.post("/servicios-mes")
def servicios_mes(body: dict, current_user=Depends(get_current_user)):
    anio = body.get("anio"); mes = body.get("mes")
    if not anio or not mes:
        raise HTTPException(status_code=400, detail="anio y mes requeridos")
    return service.servicios_por_mes(anio, mes)

@router.post("/citas-barbero-mes")
def citas_barbero_mes(body: dict, current_user=Depends(get_current_user)):
    id_barbero = body.get("id_barbero"); anio = body.get("anio"); mes = body.get("mes")
    if not id_barbero or not anio or not mes:
        raise HTTPException(status_code=400, detail="id_barbero, anio y mes requeridos")
    return service.citas_por_barbero_mes(id_barbero, anio, mes)

@router.post("/cancelaciones-mes")
def cancelaciones_mes(body: dict, current_user=Depends(get_current_user)):
    anio = body.get("anio"); mes = body.get("mes")
    if not anio or not mes:
        raise HTTPException(status_code=400, detail="anio y mes requeridos")
    return service.cancelaciones_mes(anio, mes)
