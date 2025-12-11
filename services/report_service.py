class ReportService:
    def __init__(self, db):
        self.db = db

    def servicios_por_mes(self, anio, mes):
        # assume pa_reporte_servicios_mes(anio, mes, p_cursor)
        conn = self.db.pool.acquire()
        try:
            cur = conn.cursor()
            out_cur = conn.cursor()
            cur.execute("BEGIN pa_reporte_servicios_mes(:p_anio, :p_mes, :p_cursor); END;", {"p_anio": anio, "p_mes": mes, "p_cursor": out_cur})
            rows = out_cur.fetchall()
            data = self.db.map_cursor_description(out_cur, rows)
            out_cur.close()
            return data
        finally:
            self.db.pool.release(conn)

    def citas_por_barbero_mes(self, id_barbero, anio, mes):
        conn = self.db.pool.acquire()
        try:
            cur = conn.cursor()
            out_cur = conn.cursor()
            cur.execute("BEGIN pa_reporte_citas_barbero_mes(:p_id_barbero, :p_anio, :p_mes, :p_cursor); END;", {"p_id_barbero": id_barbero, "p_anio": anio, "p_mes": mes, "p_cursor": out_cur})
            rows = out_cur.fetchall()
            data = self.db.map_cursor_description(out_cur, rows)
            out_cur.close()
            return data
        finally:
            self.db.pool.release(conn)

    def cancelaciones_mes(self, anio, mes):
        conn = self.db.pool.acquire()
        try:
            cur = conn.cursor()
            out_cur = conn.cursor()
            cur.execute("BEGIN pa_reporte_cancelaciones_mes(:p_anio, :p_mes, :p_cursor); END;", {"p_anio": anio, "p_mes": mes, "p_cursor": out_cur})
            rows = out_cur.fetchall()
            data = self.db.map_cursor_description(out_cur, rows)
            out_cur.close()
            return data
        finally:
            self.db.pool.release(conn)
