from fastapi import FastAPI
from db import get_connection

app = FastAPI()

@app.get("/")
def root():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT NOW() AS fecha;")
        row = cursor.fetchone()
        conn.close()

        return {
            "mensaje": "FastAPI + MySQL funcionando correctamente",
            "fecha_mysql": str(row["fecha"])
        }

    except Exception as e:
        print("Error:", e)
        return {"error": "Error conectando a MySQL"}
