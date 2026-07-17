# Plantilla de sitio estático con Nginx

Entorno de desarrollo para publicar archivos HTML, CSS y JavaScript mediante
Nginx. Incluye una página mínima en `app/index.html` que puede reemplazarse por
el contenido del proyecto.

> Esta plantilla está pensada para desarrollo, demostraciones y laboratorio.
> No corresponde a una configuración Nginx endurecida para producción.

## Servicios

- `app`: Nginx Alpine con el contenido estático montado desde `app/`.
- Red externa dedicada para conectarse con Nginx Proxy Manager.
- No utiliza base de datos ni panel de administración.

## Generación

Desde el directorio `automatizacion/`:

```bash
make crear nombre=demo_static stack=static_nginx
```

El generador crea `.env`, prepara la red del proxy e inicia el contenedor. El
servicio expone el puerto `80` únicamente dentro de la red Docker.

## Operación

```bash
make ps       # Revisar estado
make logs     # Seguir logs
make restart  # Reiniciar Nginx
make shell    # Abrir una terminal en el contenedor
make down     # Detener el servicio
```

`make destroy` detiene el contenedor y desconecta la red externa.

## Validación

```bash
docker compose config
make ps
```

La publicación mediante dominio y TLS se configura posteriormente en Nginx
Proxy Manager. No incluye pipeline de despliegue, caché avanzada, cabeceras de
seguridad ni observabilidad productiva.
