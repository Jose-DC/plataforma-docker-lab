from flask import Flask
from db import get_connection

app = Flask(__name__)

@app.get("/")
def index():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT NOW() AS fecha;")
        row = cursor.fetchone()
        conn.close()

        return f"""
            Flask + MySQL funcionando correctamente<br>
            Fecha en MySQL: {row['fecha']}
        """
    except Exception as e:
        print("Error:", e)
        return "Error conectando a MySQL ", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
