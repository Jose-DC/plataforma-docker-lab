# Plantilla Laravel + MySQL

Entorno de desarrollo para una aplicación Laravel con MySQL. Utiliza la imagen
de terceros `shinsenter/laravel:php8.3-nginx` como base de ejecución.

> Esta plantilla está pensada para desarrollo y laboratorio. La imagen de
> Laravel no es oficial y el entorno no está preparado para producción.

## Servicios

- `app`: entorno Laravel con PHP 8.3 y Nginx.
- `db`: MySQL con volumen persistente y healthcheck.
- `phpmyadmin`: panel opcional, habilitado mediante un perfil de Compose.
- Red interna para aplicación y base de datos, más una red externa para el proxy.

## Generación

Desde el directorio `automatizacion/`:

```bash
make crear nombre=demo_laravel_mysql stack=laravel+mysql dbv=8.0
```

El generador crea `.env`, genera una `APP_KEY` y contraseñas locales, e inicia
los servicios principales. El código debe agregarse posteriormente al
directorio de aplicación generado.

## Operación

```bash
make ps            # Revisar estado
make logs          # Seguir logs
make restart       # Reiniciar el entorno
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

La plantilla no incorpora una aplicación Laravel terminada, despliegue
productivo, copias de seguridad, alta disponibilidad ni gestión externa de
secretos.
