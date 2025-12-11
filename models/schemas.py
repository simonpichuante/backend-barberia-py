from pydantic import BaseModel
from typing import Optional

class ClienteCreate(BaseModel):
    RUT: str
    NOMBRE: str
    APELLIDO: Optional[str] = None
    CORREO: Optional[str] = None
    CELULAR: Optional[str] = None

class BarberoCreate(BaseModel):
    NOMBRE: str
    APELLIDO: Optional[str] = None
    EXPERIENCIA: Optional[int] = 0

class SolicitudCreate(BaseModel):
    ID_CLIENTE: Optional[int]
    NOMBRE_CLIENTE: Optional[str]
    TELEFONO: Optional[str]
    ID_SERVICIO: int
    FECHA: Optional[str]

class CitaCreate(BaseModel):
    ID_CLIENTE: int
    ID_SERVICIO: int
    ID_BARBERO: int
    ID_HORA: int
    FECHA: str
