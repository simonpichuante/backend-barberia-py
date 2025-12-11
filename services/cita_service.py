from db import get_conn, refcursor_to_list
import oracledb

def list_citas():
    with get_conn() as conn:
        cur = conn.cursor()
        outcur = cur.var(oracledb.DB_TYPE_CURSOR)
        cur.callproc("pa_cita_list", [outcur])
        rc = outcur.getvalue()
        result = refcursor_to_list(rc)
        rc.close()
        cur.close()
        return result

def get_cita(p_id):
    with get_conn() as conn:
        cur = conn.cursor()
        outcur = cur.var(oracledb.DB_TYPE_CURSOR)
        cur.callproc("pa_cita_get", [p_id, outcur])
        rc = outcur.getvalue()
        rows = refcursor_to_list(rc)
        rc.close()
        cur.close()
        return rows[0] if rows else None

def insert_cita(p_id_solicitud, p_id_cliente, p_id_servicio, p_id_barbero, p_fecha_programada, p_observaciones):
    with get_conn() as conn:
        cur = conn.cursor()
        # Usamos el procedimiento pa_cita_insert definido en tu DDL
        # p_fecha_programada debe ser un datetime compatible con oracledb
        cur.callproc("pa_cita_insert", [p_id_solicitud, p_id_cliente, p_id_servicio, p_id_barbero, p_fecha_programada, p_observaciones])
        cur.close()
        return True

def delete_cita(p_id):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.callproc("pa_cita_delete", [p_id])
        cur.close()
        return True

# Gestores
def convertir_solicitud_a_cita(p_id_solicitud, p_id_hora_disponible):
    with get_conn() as conn:
        cur = conn.cursor()
        # gestor_convertir_solicitud_a_cita(p_id_solicitud, p_id_hora_disponible)
        cur.callproc("gestor_convertir_solicitud_a_cita", [p_id_solicitud, p_id_hora_disponible])
        cur.close()
        return True

def asignar_barbero_automatico(p_id_cita):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.callproc("gestor_asignar_barbero_automatico", [p_id_cita])
        cur.close()
        return True

def finalizar_cita(p_id_cita, p_notas):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.callproc("gestor_finalizar_cita", [p_id_cita, p_notas])
        cur.close()
        return True

def cancelar_cita(p_id_cita, p_motivo):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.callproc("gestor_cancelar_cita", [p_id_cita, p_motivo])
        cur.close()
        return True

def reprogramar_cita(p_id_cita, p_nueva_fecha, p_id_hora_nueva):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.callproc("gestor_reprogramar_cita", [p_id_cita, p_nueva_fecha, p_id_hora_nueva])
        cur.close()
        return True
