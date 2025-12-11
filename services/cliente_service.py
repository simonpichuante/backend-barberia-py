from db import get_conn, refcursor_to_list
import oracledb

def list_clientes():
    with get_conn() as conn:
        cur = conn.cursor()
        outcur = cur.var(oracledb.DB_TYPE_CURSOR)
        cur.callproc("pa_cliente_list", [outcur])
        rc = outcur.getvalue()
        result = refcursor_to_list(rc)
        rc.close()
        cur.close()
        return result

def get_cliente(p_id: int):
    with get_conn() as conn:
        cur = conn.cursor()
        outcur = cur.var(oracledb.DB_TYPE_CURSOR)
        cur.callproc("pa_cliente_get", [p_id, outcur])
        rc = outcur.getvalue()
        rows = refcursor_to_list(rc)
        rc.close()
        cur.close()
        return rows[0] if rows else None

def insert_cliente(p_rut, p_nombre, p_apellido=None, p_correo=None, p_celular=None):
    with get_conn() as conn:
        cur = conn.cursor()
        # pa_cliente_insert(p_rut, p_nombre, p_apellido, p_correo, p_celular)
        cur.callproc("pa_cliente_insert", [p_rut, p_nombre, p_apellido, p_correo, p_celular])
        # procedure commits internally per DDL you shared
        cur.close()
        return True

def update_cliente(p_id, p_rut, p_nombre, p_apellido=None, p_correo=None, p_celular=None):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.callproc("pa_cliente_update", [p_id, p_rut, p_nombre, p_apellido, p_correo, p_celular])
        cur.close()
        return True

def delete_cliente(p_id):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.callproc("pa_cliente_delete", [p_id])
        cur.close()
        return True
