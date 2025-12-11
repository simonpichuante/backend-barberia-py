from services.base_service import BaseService
from exceptions.custom_exceptions import NotFoundError

class ClienteService(BaseService):
    def create(self, payload):
        # llamamos al procedimiento pa_cliente_insert SI existe en la BD
        # si no existe, fallback a insert directo
        try:
            # ejemplo de llamada a procedimiento: pa_cliente_insert(:p_rut, :p_nombre, :p_apellido, :p_correo, :p_celular)
            plsql = "BEGIN pa_cliente_insert(:p_rut, :p_nombre, :p_apellido, :p_correo, :p_celular); END;"
            params = {
                "p_rut": payload.get("RUT"),
                "p_nombre": payload.get("NOMBRE"),
                "p_apellido": payload.get("APELLIDO"),
                "p_correo": payload.get("CORREO"),
                "p_celular": payload.get("CELULAR")
            }
            return self.db.execute_object(plsql, params)
        except Exception:
            sql = "INSERT INTO CLIENTE (RUT, NOMBRE, APELLIDO, CORREO, CELULAR) VALUES (:RUT,:NOMBRE,:APELLIDO,:CORREO,:CELULAR)"
            return self.db.execute_object(sql, payload)

    def update(self, id_, payload):
        sql = "UPDATE CLIENTE SET RUT=:RUT, NOMBRE=:NOMBRE, APELLIDO=:APELLIDO, CORREO=:CORREO, CELULAR=:CELULAR WHERE ID_CLIENTE=:id"
        p = payload.copy()
        p["id"] = id_
        return self.db.execute_object(sql, p)

    def delete(self, id_):
        return self.db.execute_object("DELETE FROM CLIENTE WHERE ID_CLIENTE=:id", {"id": id_})

    def get(self, id_):
        rows = self.db.execute_object("SELECT * FROM CLIENTE WHERE ID_CLIENTE=:id", {"id": id_})
        if not rows:
            raise NotFoundError("Cliente no encontrado")
        return rows[0]

    def list(self, **filters):
        return self.db.execute_object("SELECT * FROM CLIENTE ORDER BY NOMBRE")
