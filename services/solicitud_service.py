from services.base_service import BaseService
from exceptions.custom_exceptions import NotFoundError

class SolicitudService(BaseService):
    def create(self, payload):
        # Use stored procedure pa_solicitud_insert if exists
        try:
            plsql = "BEGIN pa_solicitud_insert(:p_id_cliente, :p_nombre, :p_telefono, :p_id_servicio, :p_fecha); END;"
            params = {
                "p_id_cliente": payload.get("ID_CLIENTE"),
                "p_nombre": payload.get("NOMBRE_CLIENTE"),
                "p_telefono": payload.get("TELEFONO"),
                "p_id_servicio": payload.get("ID_SERVICIO"),
                "p_fecha": payload.get("FECHA")
            }
            return self.db.execute_object(plsql, params)
        except Exception:
            sql = "INSERT INTO SOLICITUD_CITA (ID_CLIENTE, NOMBRE_CLIENTE, TELEFONO, ID_SERVICIO, FECHA) VALUES (:ID_CLIENTE, :NOMBRE_CLIENTE, :TELEFONO, :ID_SERVICIO, TO_DATE(:FECHA,'YYYY-MM-DD'))"
            return self.db.execute_object(sql, payload)

    def update(self, id_, payload):
        sql = "UPDATE SOLICITUD_CITA SET ID_CLIENTE=:ID_CLIENTE, NOMBRE_CLIENTE=:NOMBRE_CLIENTE, TELEFONO=:TELEFONO, ID_SERVICIO=:ID_SERVICIO, FECHA=TO_DATE(:FECHA,'YYYY-MM-DD') WHERE ID_SOLICITUD=:id"
        p = payload.copy(); p["id"]=id_
        return self.db.execute_object(sql,p)

    def delete(self, id_):
        return self.db.execute_object("DELETE FROM SOLICITUD_CITA WHERE ID_SOLICITUD=:id", {"id": id_})

    def get(self, id_):
        rows = self.db.execute_object("SELECT * FROM SOLICITUD_CITA WHERE ID_SOLICITUD=:id", {"id": id_})
        if not rows:
            raise NotFoundError("Solicitud no encontrada")
        return rows[0]

    def list(self, **filters):
        return self.db.execute_object("SELECT * FROM SOLICITUD_CITA ORDER BY FECHA DESC")
