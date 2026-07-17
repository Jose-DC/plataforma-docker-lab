# Plantilla Moodle + MySQL

Entorno de desarrollo para probar Moodle con MySQL. La imagen de la aplicación
se construye desde `app/Dockerfile` usando la rama indicada en `.env`.

> Esta plantilla está pensada para desarrollo y laboratorio. No representa una
> instalación Moodle endurecida ni preparada para producción.

## Servicios

- `app`: Moodle con servidor web, construido localmente.
- `db`: MySQL con volumen persistente y healthcheck.
- `phpmyadmin`: panel opcional, habilitado mediante un perfil de Compose.
- Red interna para aplicación y base de datos, más una red externa para el proxy.

## Generación

Desde el directorio `automatizacion/`:

```bash
make crear nombre=demo_moodle_mysql stack=moodle+mysql dbv=8.0
```

El generador crea `.env`, asigna credenciales locales e inicia los servicios.
La instalación funcional de Moodle se completa desde su interfaz web.

## Operación

```bash
make prepare       # Preparar permisos locales si son necesarios
make rebuild       # Construir nuevamente la aplicación
make ps            # Revisar estado
make logs          # Seguir logs
make phpmyadmin    # Iniciar el panel opcional
make down          # Detener servicios
```

`make destroy` elimina contenedores y volúmenes. Úsalo solo cuando los datos y
archivos del laboratorio puedan descartarse.

## Validación

```bash
docker compose config
make ps
```

No incluye correo, cron operativo, respaldos, alta disponibilidad,
actualizaciones automáticas ni endurecimiento productivo.
