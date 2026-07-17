# Plantilla WordPress + MySQL

Entorno de desarrollo para ejecutar WordPress con MySQL y almacenamiento
persistente. La configuración inicial de WordPress se completa desde su
interfaz web.

> Esta plantilla está pensada para desarrollo y laboratorio. No representa un
> sitio WordPress endurecido ni preparado para producción.

## Servicios

- `wordpress`: WordPress con Apache.
- `db`: MySQL con volumen persistente y healthcheck.
- `phpmyadmin`: panel opcional, habilitado mediante un perfil de Compose.
- Red interna para WordPress y MySQL, más una red externa para el proxy.

## Generación

Desde el directorio `automatizacion/`:

```bash
make crear nombre=demo_wordpress stack=wordpress+mysql dbv=8.0
```

El generador crea `.env`, asigna credenciales locales e inicia los servicios.
WordPress expone el puerto `80` solo dentro de las redes Docker.

## Operación

```bash
make ps            # Revisar estado
make logs          # Seguir logs
make restart       # Reiniciar el entorno
make phpmyadmin    # Iniciar el panel opcional
make shell         # Abrir una terminal en WordPress
make down          # Detener servicios
```

`make destroy` elimina contenedores y volúmenes. Úsalo solo cuando el contenido
y la base de datos del laboratorio puedan descartarse.

## Validación

```bash
docker compose config
make ps
```

No incluye copias de seguridad, correo, actualizaciones controladas, caché,
protección adicional de acceso ni endurecimiento productivo.
