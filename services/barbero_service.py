from services.base_service import BaseService
from exceptions.custom_exceptions import NotFoundError

class BarberoService(BaseService):
    def create(self, payload):
        # Use procedure if exists: pa_barbero_insert(name, surname, out_id)
        # Fallback to direct insert
        sql = "INSERT INTO BARBERO (NOMBRE, APELLIDO, EXPERIENCIA) VALUES (:NOMBRE, :APELLIDO, :EXPERIENCIA)"
        return self.db.execute_object(sql, payload)

    def update(self, id_, payload):
        sql = "UPDATE BARBERO SET NOMBRE=:NOMBRE, APELLIDO=:APELLIDO, EXPERIENCIA=:EXPERIENCIA WHERE ID_BARBERO=:id"
        p = payload.copy()
        p["id"] = id_
        return self.db.execute_object(sql, p)

    def delete(self, id_):
        return self.db.execute_object("DELETE FROM BARBERO WHERE ID_BARBERO=:id", {"id": id_})

    def get(self, id_):
        rows = self.db.execute_object("SELECT * FROM BARBERO WHERE ID_BARBERO=:id", {"id": id_})
        if not rows:
            raise NotFoundError("Barbero no encontrado")
        return rows[0]

    def list(self, **filters):
        return self.db.execute_object("SELECT * FROM BARBERO ORDER BY NOMBRE")
