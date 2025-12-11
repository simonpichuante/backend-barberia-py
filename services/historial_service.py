from services.base_service import BaseService
from exceptions.custom_exceptions import NotFoundError

class HistorialService(BaseService):
    def create(self, payload):
        sql = "INSERT INTO HISTORIAL (ID_CLIENTE, ID_SERVICIO, FECHA, DETALLE) VALUES (:ID_CLIENTE, :ID_SERVICIO, TO_DATE(:FECHA,'YYYY-MM-DD'), :DETALLE)"
        return self.db.execute_object(sql, payload)

    def update(self, id_, payload):
        sql = "UPDATE HISTORIAL SET ID_CLIENTE=:ID_CLIENTE, ID_SERVICIO=:ID_SERVICIO, FECHA=TO_DATE(:FECHA,'YYYY-MM-DD'), DETALLE=:DETALLE WHERE ID_HISTORIAL=:id"
        p = payload.copy(); p["id"]=id_
        return self.db.execute_object(sql,p)

    def delete(self, id_):
        return self.db.execute_object("DELETE FROM HISTORIAL WHERE ID_HISTORIAL=:id", {"id": id_})

    def get(self, id_):
        rows = self.db.execute_object("SELECT * FROM HISTORIAL WHERE ID_HISTORIAL=:id", {"id": id_})
        if not rows:
            raise NotFoundError("Historial no encontrado")
        return rows[0]

    def list(self, **filters):
        return self.db.execute_object("SELECT * FROM HISTORIAL ORDER BY FECHA DESC")
