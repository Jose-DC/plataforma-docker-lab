from flask import Flask
from db import get_connection

app = Flask(__name__)

@app.get("/")
def index():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT NOW() AS fecha;")
        row = cur.fetchone()
        conn.close()

        return f"""
            Flask + PostgreSQL funcionando correctamente<br>
            Fecha en PostgreSQL: {row['fecha']}
        """
    except Exception as e:
        print("Error:", e)
        return "Error conectando a PostgreSQL", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
