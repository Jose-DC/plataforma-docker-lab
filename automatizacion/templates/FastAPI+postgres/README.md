# Plantilla FastAPI + PostgreSQL

Entorno de desarrollo para una API mínima con FastAPI y persistencia en
PostgreSQL. La aplicación de ejemplo valida el arranque y la conexión con la
base de datos.

> Esta plantilla está pensada para desarrollo y laboratorio. No incluye las
> medidas necesarias para operar una aplicación en producción.

## Servicios

- `app`: aplicación FastAPI construida desde `app/Dockerfile`.
- `db`: PostgreSQL con volumen persistente y healthcheck.
- `pgadmin`: panel opcional, habilitado mediante un perfil de Compose.
- Red interna para aplicación y base de datos, más una red externa para el proxy.

## Generación

Desde el directorio `automatizacion/`:

```bash
make crear nombre=demo_fastapi_postgres stack=FastAPI+postgres lang=3.12 dbv=16
```

El generador crea `.env`, asigna secretos locales e inicia los servicios
principales. La aplicación expone el puerto `80` solo dentro de las redes Docker.

## Operación

```bash
make ps          # Revisar estado
make logs        # Seguir logs
make rebuild     # Reconstruir la aplicación
make pgadmin     # Iniciar el panel opcional
make down        # Detener servicios
```

`make destroy` elimina contenedores, volúmenes y la red interna. Úsalo solo
cuando los datos del entorno puedan descartarse.

## Validación

```bash
docker compose config
make ps
```

La publicación mediante dominio y TLS se configura posteriormente en Nginx
Proxy Manager. No incluye alta disponibilidad, copias de seguridad ni gestión
centralizada de secretos.
