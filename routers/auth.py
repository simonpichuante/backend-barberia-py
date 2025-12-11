from fastapi import APIRouter, HTTPException
from config import db
import bcrypt
from core.auth import create_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register_barbero")
def register_barbero(body: dict):
    nombre = body.get("nombre")
    apellido = body.get("apellido")
    username = body.get("username")
    password = body.get("password")
    if not nombre or not username or not password:
        raise HTTPException(status_code=400, detail="nombre, username y password son requeridos")

    # Crear barbero
    db.execute_object("INSERT INTO BARBERO (NOMBRE, APELLIDO) VALUES (:NOMBRE, :APELLIDO)", {"NOMBRE": nombre, "APELLIDO": apellido})
    # Conseguir id insertado (mejor usar sequence + returning en tu BD; aquí buscamos último por nombre/apellido)
    rows = db.execute_object("SELECT ID_BARBERO FROM BARBERO WHERE NOMBRE=:NOMBRE AND APELLIDO=:APELLIDO ORDER BY ID_BARBERO DESC", {"NOMBRE": nombre, "APELLIDO": apellido})
    id_barbero = rows[0]["ID_BARBERO"]
    phash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    db.execute_object("INSERT INTO USERS (ID_BARBERO, USERNAME, PASSWORD_HASH, ROLE) VALUES (:idb, :u, :ph, 'BARBERO')", {"idb": id_barbero, "u": username, "ph": phash})
    return {"ok": True, "id_barbero": id_barbero}

@router.post("/login")
def login(body: dict):
    username = body.get("username")
    password = body.get("password")
    if not username or not password:
        raise HTTPException(status_code=400, detail="Faltan credenciales")
    rows = db.execute_object("SELECT * FROM USERS WHERE USERNAME=:u", {"u": username})
    if not rows:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    user = rows[0]
    phash = user["PASSWORD_HASH"]
    if not bcrypt.checkpw(password.encode(), phash.encode()):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    token = create_token({"sub": user["ID_USER"], "id_barbero": user["ID_BARBERO"], "role": user["ROLE"]})
    return {"token": token, "user": {"id_user": user["ID_USER"], "id_barbero": user["ID_BARBERO"], "role": user["ROLE"]}}
