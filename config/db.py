import os
import oracledb
from dotenv import load_dotenv

load_dotenv()

try:
    # solo si necesitas init
    oracledb.init_oracle_client()
except Exception:
    pass

class OracleDB:
    def __init__(self):
        self.pool = None

    def init(self):
        if self.pool:
            return
        self.pool = oracledb.create_pool(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            dsn=os.getenv("DB_CONNECT"),
            min=1, max=10, increment=1
        )
        print("✓ Pool de conexiones Oracle inicializado")

    def map_cursor_description(self, cursor, rows):
        if not rows or not cursor.description:
            return []
        columns = [d[0] for d in cursor.description]
        return [dict(zip(columns, row)) for row in rows]

    def execute_object(self, sql, params=None, auto_commit=True):
        conn = self.pool.acquire()
        try:
            cur = conn.cursor()
            cur.execute(sql, params or {})
            if cur.description:
                rows = cur.fetchall()
                return self.map_cursor_description(cur, rows)
            else:
                if auto_commit:
                    conn.commit()
                return {"rows_affected": cur.rowcount}
        finally:
            try:
                cur.close()
            except Exception:
                pass
            try:
                self.pool.release(conn)
            except Exception:
                pass

    def execute_proc_cursor(self, plsql, bind_vars):
        """
        Ejecuta un PL/SQL que retorna un REF CURSOR en bind_vars['p_cursor'].
        plsql: "BEGIN pa_xxx(:p_in1, :p_cursor); END;"
        bind_vars: dict con claves y valores; se debe incluir un cursor creado por conn.cursor()
        """
        conn = self.pool.acquire()
        try:
            cur = conn.cursor()
            # se espera que bind_vars contenga un cursor de salida (out cursor)
            cur.execute(plsql, bind_vars)
            # localizar cursor en bind_vars
            out_cursor = None
            for v in bind_vars.values():
                if hasattr(v, "fetchall") and hasattr(v, "description"):
                    out_cursor = v
                    break
            if out_cursor is None:
                return []
            rows = out_cursor.fetchall()
            data = self.map_cursor_description(out_cursor, rows)
            out_cursor.close()
            return data
        finally:
            try:
                cur.close()
            except Exception:
                pass
            try:
                self.pool.release(conn)
            except Exception:
                pass

# singleton
db = OracleDB()
