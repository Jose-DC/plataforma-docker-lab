const express = require("express");
const pool = require("./db");
const app = express();

app.get("/", async (req, res) => {
  try {
    const [rows] = await pool.query("SELECT NOW() AS fecha");
    res.send(`
      🟩 Node.js + MySQL funcionando correctamente<br>
      Fecha servidor MySQL: ${rows[0].fecha}
    `);
  } catch (err) {
    console.error("Error ejecutando consulta:", err);
    res.status(500).send("Error conectando a MySQL ❌");
  }
});

// Puerto interno expuesto al proxy
const PORT = 80;
app.listen(PORT, () => {
  console.log(`Servidor Node escuchando en puerto ${PORT}`);
});
