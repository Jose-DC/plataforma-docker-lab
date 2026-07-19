from fastapi import FastAPI
from db import get_connection

app = FastAPI()

@app.get("/")
def root():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT NOW() AS fecha;")
        row = cur.fetchone()
        conn.close()

        return {
            "mensaje": "FastAPI + PostgreSQL funcionando correctamente",
            "fecha_postgres": str(row["fecha"])
        }
    except Exception as e:
        print("Error:", e)
        return {"error": "Error conectando a PostgreSQL"}
