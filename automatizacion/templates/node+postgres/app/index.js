const express = require("express");
const pool = require("./db");
const app = express();

app.get("/", async (req, res) => {
  try {
    const result = await pool.query("SELECT NOW() as fecha");
    res.send(`
      🟪 Node.js + PostgreSQL funcionando correctamente<br>
      Fecha servidor PostgreSQL: ${result.rows[0].fecha}
    `);
  } catch (err) {
    console.error("Error ejecutando consulta:", err);
    res.status(500).send("Error conectando a PostgreSQL ❌");
  }
});

// Puerto interno expuesto al proxy
const PORT = 80;
app.listen(PORT, () => {
  console.log("Servidor Node escuchando en puerto 80");
});
