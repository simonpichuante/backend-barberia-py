from services.base_service import BaseService
from exceptions.custom_exceptions import NotFoundError, ForbiddenError

class CitaService(BaseService):
    def create(self, payload):
        # preferir gestor o procedimiento que cree la cita correctamente
        try:
            # si hay un gestor: gestor_convertir_solicitud_a_cita o pa_cita_insert
            plsql = "BEGIN pa_cita_insert(:p_id_cliente, :p_id_servicio, :p_id_barbero, :p_id_hora, :p_fecha); END;"
            params = {
                "p_id_cliente": payload.get("ID_CLIENTE"),
                "p_id_servicio": payload.get("ID_SERVICIO"),
                "p_id_barbero": payload.get("ID_BARBERO"),
                "p_id_hora": payload.get("ID_HORA"),
                "p_fecha": payload.get("FECHA")
            }
            return self.db.execute_object(plsql, params)
        except Exception:
            sql = "INSERT INTO CITA (ID_CLIENTE, ID_SERVICIO, ID_BARBERO, ID_HORA, FECHA) VALUES (:ID_CLIENTE, :ID_SERVICIO, :ID_BARBERO, :ID_HORA, TO_DATE(:FECHA,'YYYY-MM-DD'))"
            return self.db.execute_object(sql, payload)

    def update(self, id_, payload, current_barbero_id=None, current_role="BARBERO"):
        if current_role != "ADMIN":
            rows = self.db.execute_object("SELECT ID_BARBERO FROM CITA WHERE ID_CITA=:id", {"id": id_})
            if not rows:
                raise NotFoundError("Cita no encontrada")
            if rows[0]["ID_BARBERO"] != current_barbero_id:
                raise ForbiddenError("No puedes actualizar citas de otros barberos")
        # preferir pa_cita_update si existe
        try:
            plsql = "BEGIN pa_cita_update(:p_id_cita, :p_id_servicio, :p_id_hora, :p_fecha); END;"
            params = {"p_id_cita": id_, "p_id_servicio": payload.get("ID_SERVICIO"), "p_id_hora": payload.get("ID_HORA"), "p_fecha": payload.get("FECHA")}
            return self.db.execute_object(plsql, params)
        except Exception:
            sql = "UPDATE CITA SET ID_SERVICIO=:ID_SERVICIO, ID_HORA=:ID_HORA, FECHA=TO_DATE(:FECHA,'YYYY-MM-DD') WHERE ID_CITA=:id"
            p = payload.copy(); p["id"]=id_
            return self.db.execute_object(sql,p)

    def delete(self, id_, current_barbero_id=None, current_role="BARBERO"):
        if current_role != "ADMIN":
            rows = self.db.execute_object("SELECT ID_BARBERO FROM CITA WHERE ID_CITA=:id", {"id": id_})
            if not rows:
                raise NotFoundError("Cita no encontrada")
            if rows[0]["ID_BARBERO"] != current_barbero_id:
                raise ForbiddenError("No puedes eliminar citas de otros barberos")
        # preferir gestor_cancelar_cita
        try:
            plsql = "BEGIN gestor_cancelar_cita(:p_id_cita); END;"
            return self.db.execute_object(plsql, {"p_id_cita": id_})
        except Exception:
            return self.db.execute_object("DELETE FROM CITA WHERE ID_CITA=:id", {"id": id_})

    def get(self, id_):
        rows = self.db.execute_object("SELECT * FROM CITA WHERE ID_CITA=:id", {"id": id_})
        if not rows:
            raise NotFoundError("Cita no encontrada")
        return rows[0]

    def list(self, current_barbero_id=None, role="BARBERO"):
        if role == "ADMIN":
            return self.db.execute_object("SELECT * FROM CITA ORDER BY FECHA DESC")
        if current_barbero_id:
            return self.db.execute_object("SELECT * FROM CITA WHERE ID_BARBERO=:id ORDER BY FECHA DESC", {"id": current_barbero_id})
        return []
