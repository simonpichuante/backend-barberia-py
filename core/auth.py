import os
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Header

JWT_SECRET = os.getenv("JWT_SECRET", "cambiame")
JWT_EXP_HOURS = int(os.getenv("JWT_EXP_HOURS", "8"))

def create_token(payload: dict):
    exp = datetime.utcnow() + timedelta(hours=JWT_EXP_HOURS)
    payload2 = payload.copy()
    payload2["exp"] = exp
    token = jwt.encode(payload2, JWT_SECRET, algorithm="HS256")
    return token

def decode_token(token: str):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")

def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Falta cabecera Authorization")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Formato Authorization inválido")
    token = authorization.split(" ")[1]
    return decode_token(token)
