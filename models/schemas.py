from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# CLIENTE
class ClienteBase(BaseModel):
    rut: Optional[str]
    nombre: str
    apellido: Optional[str] = None
    correo: Optional[str] = None
    celular: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteOut(ClienteBase):
    id_cliente: int

# BARBERO (solo esquema básico)
class BarberoOut(BaseModel):
    id_barbero: int
    usuario: str
    nombre: Optional[str]
    activo: Optional[str]

# SERVICIO
class ServicioBase(BaseModel):
    nombre: str
    duracion_min: int
    precio: float

class ServicioOut(ServicioBase):
    id_servicio: int

# SOLICITUD_CITA minimal
class SolicitudCreate(BaseModel):
    id_cliente: int
    fecha_cita_solicitada: Optional[datetime] = None
    id_servicio: Optional[int] = None
    fecha_limite: Optional[datetime] = None

# CITA
class CitaCreate(BaseModel):
    id_solicitud: Optional[int] = None
    id_cliente: Optional[int] = None
    id_servicio: Optional[int] = None
    id_barbero: Optional[int] = None
    fecha_programada: Optional[datetime] = None
    observaciones: Optional[str] = None

class CitaOut(BaseModel):
    id_cita: int
    id_cliente: Optional[int]
    id_servicio: Optional[int]
    id_barbero: Optional[int]
    fecha_programada: Optional[datetime]
    estado: Optional[str]
    observaciones: Optional[str]
