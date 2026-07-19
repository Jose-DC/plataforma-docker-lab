const { Pool } = require("pg");

const pool = new Pool({
  host: process.env.POSTGRES_HOST || "db",
  user: process.env.POSTGRES_USER,
  password: process.env.POSTGRES_PASSWORD,
  database: process.env.POSTGRES_DB,
  port: 5432,
  max: 10,
});

module.exports = pool;
