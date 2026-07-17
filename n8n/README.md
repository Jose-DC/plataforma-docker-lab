# n8n - Servicio de automatizacion

Este directorio contiene un ejemplo de servicio n8n con PostgreSQL, pensado para ejecutarse dentro de la plataforma Docker y conectarse al proxy inverso mediante la red externa `proxy_n8n_net`.

La configuracion esta preparada como ejemplo de despliegue. Las credenciales reales deben definirse en un archivo `.env` local, que no se versiona.

## Componentes

- `n8n`: aplicacion principal de automatizacion.
- `db`: base de datos PostgreSQL para persistencia.
- `n8n_net`: red interna entre n8n y PostgreSQL.
- `proxy_n8n_net`: red externa usada por el proxy inverso.
- `n8n_app_data`: volumen persistente de configuracion interna de n8n.
- `n8n_db_data`: volumen persistente de PostgreSQL.

## Uso basico

Crear el archivo `.env` desde la plantilla:

```bash
cp .env.example .env
```

Editar los valores `change-me` antes de levantar el stack:

```bash
docker network create proxy_n8n_net
docker compose up -d
docker compose ps
```

## Exposicion del servicio

El contenedor no publica el puerto `5678` directamente al host. El acceso esperado es mediante el proxy inverso conectado a `proxy_n8n_net`.

## Seguridad

- No subir `.env`.
- No versionar datos internos de n8n ni claves de cifrado.
- Definir `WEBHOOK_URL` con el dominio real solo en el entorno local o servidor.
- Revisar permisos y acceso al panel antes de exponerlo mediante proxy.
