# Plantilla LimeSurvey + MySQL

Entorno de desarrollo y evaluación para ejecutar LimeSurvey con MySQL. Utiliza
la imagen de terceros `acspri/limesurvey:6.15.23`.

> Esta plantilla está pensada para desarrollo y laboratorio. La imagen y la
> configuración deben revisarse; el entorno no está preparado para producción.

## Servicios

- `app`: instancia de LimeSurvey.
- `init`: preparación inicial de los directorios compartidos.
- `db`: MySQL con volumen persistente y healthcheck.
- `phpmyadmin`: panel opcional, habilitado mediante un perfil de Compose.
- Red interna para servicios, más una red externa para el proxy.

## Generación

Desde el directorio `automatizacion/`:

```bash
make crear nombre=demo_limesurvey stack=limesurvey+mysql dbv=8.0
```

El generador crea `.env`, asigna credenciales locales e inicia los servicios
principales. LimeSurvey expone el puerto `80` solo dentro de las redes Docker.

## Operación

```bash
make ps            # Revisar estado
make logs          # Seguir logs
make restart       # Reiniciar el entorno
make phpmyadmin    # Iniciar el panel opcional
make down          # Detener servicios
```

`make destroy` elimina contenedores, volúmenes y la red interna. Úsalo solo
cuando las encuestas y datos del laboratorio puedan descartarse.

## Validación

```bash
docker compose config
make ps
```

No incluye estrategia de respaldo, correo, alta disponibilidad, endurecimiento
de seguridad ni mantenimiento productivo.
