from fastapi import APIRouter, Depends, HTTPException
from core.auth import get_current_user
from services.cita_service import CitaService
from config import db
from exceptions.custom_exceptions import NotFoundError, ForbiddenError

router = APIRouter(prefix="/citas", tags=["citas"])
service = CitaService(db)

@router.get("/")
def list_citas(current_user=Depends(get_current_user)):
    return service.list(current_barbero_id=current_user.get("id_barbero"), role=current_user.get("role"))

@router.get("/{id}")
def get_cita(id: int, current_user=Depends(get_current_user)):
    try:
        c = service.get(id)
        if current_user.get("role") != "ADMIN" and c["ID_BARBERO"] != current_user.get("id_barbero"):
            raise HTTPException(status_code=403, detail="No puedes ver esta cita")
        return c
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/")
def create_cita(body: dict, current_user=Depends(get_current_user)):
    # barbero crea cita o gestores la crean a partir de solicitud
    return service.create(body)

@router.put("/{id}")
def update_cita(id: int, body: dict, current_user=Depends(get_current_user)):
    try:
        return service.update(id, body, current_barbero_id=current_user.get("id_barbero"), current_role=current_user.get("role"))
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ForbiddenError as e:
        raise HTTPException(status_code=403, detail=str(e))

@router.delete("/{id}")
def delete_cita(id: int, current_user=Depends(get_current_user)):
    try:
        return service.delete(id, current_barbero_id=current_user.get("id_barbero"), current_role=current_user.get("role"))
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ForbiddenError as e:
        raise HTTPException(status_code=403, detail=str(e))
