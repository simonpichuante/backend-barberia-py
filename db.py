# db.py
import os
import oracledb
from contextlib import contextmanager
from dotenv import load_dotenv
import logging

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DSN = os.getenv("DB_DSN")  # ej: host:1521/ORCLPDB1

# pool variable global (inicialización perezosa)
_pool = None

def init_pool(min=1, max=4, increment=1):
    """
    Inicializa el pool de conexiones si aún no existe.
    Llamar en startup de la app o antes de la primera consulta.
    """
    global _pool
    if _pool is not None:
        return _pool

    if not DB_USER or not DB_PASSWORD or not DB_DSN:
        raise RuntimeError("Variables de entorno DB_USER/DB_PASSWORD/DB_DSN faltantes. Revisa .env")

    try:
        # Nota: no usar 'encoding' si la versión de oracledb no lo admite.
        _pool = oracledb.create_pool(user=DB_USER,
                                     password=DB_PASSWORD,
                                     dsn=DB_DSN,
                                     min=min,
                                     max=max,
                                     increment=increment)
        logging.info("Oracle pool creado (min=%s max=%s)", min, max)
        return _pool
    except Exception:
        logging.exception("Error inicializando el pool Oracle")
        raise

def get_pool():
    """
    Retorna el pool existente o lo inicializa.
    """
    global _pool
    if _pool is None:
        init_pool()
    return _pool

@contextmanager
def get_conn():
    """
    Context manager para obtener una conexión desde el pool.
    Uso:
      with get_conn() as conn:
          with conn.cursor() as cur:
              ...
    """
    pool = get_pool()
    conn = pool.acquire()
    try:
        yield conn
    finally:
        try:
            pool.release(conn)
        except Exception:
            # liberar silenciosamente si algo raro ocurre
            logging.exception("Error liberando conexión al pool")

def refcursor_to_list(refcur):
    """
    Convierte un cursor Oracle (resultado de SYS_REFCURSOR) a lista de dicts.
    """
    rows = refcur.fetchall()
    cols = [d[0].lower() for d in refcur.description]
    return [dict(zip(cols, r)) for r in rows]

def cursor_to_list(cur):
    rows = cur.fetchall()
    cols = [d[0].lower() for d in cur.description]
    return [dict(zip(cols, r)) for r in rows]
