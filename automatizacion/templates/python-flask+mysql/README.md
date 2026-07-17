# Plantilla Flask + MySQL

Entorno de desarrollo para una aplicación mínima en Flask con persistencia en
MySQL. El ejemplo incluido permite comprobar el arranque y la conexión con la
base de datos.

> Esta plantilla está pensada para desarrollo y laboratorio. No incluye las
> medidas necesarias para operar una aplicación en producción.

## Servicios

- `app`: aplicación Flask construida desde `app/Dockerfile`.
- `db`: MySQL con volumen persistente y healthcheck.
- `phpmyadmin`: panel opcional, habilitado mediante un perfil de Compose.
- Red interna para aplicación y base de datos, más una red externa para el proxy.

## Generación

Desde el directorio `automatizacion/`:

```bash
make crear nombre=demo_flask_mysql stack=python-flask+mysql lang=3.12 dbv=8.0
```

El generador crea `.env`, asigna secretos locales e inicia los servicios
principales. La aplicación expone el puerto `80` solo dentro de las redes Docker.

## Operación

```bash
make ps            # Revisar estado
make logs          # Seguir logs
make rebuild       # Reconstruir la aplicación
make phpmyadmin    # Iniciar el panel opcional
make shell         # Abrir una terminal en la aplicación
make down          # Detener servicios
```

`make destroy` elimina contenedores, volúmenes y la red interna. Úsalo solo
cuando los datos del entorno puedan descartarse.

## Validación

```bash
docker compose config
make ps
```

La aplicación incluida es solo una prueba técnica. No incorpora autenticación,
pruebas automatizadas, CI/CD, respaldos ni endurecimiento productivo.
