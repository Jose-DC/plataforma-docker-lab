# Proxy - Nginx Proxy Manager

Este modulo levanta Nginx Proxy Manager junto con una base de datos MariaDB. Su objetivo es centralizar la publicacion de servicios Docker mediante proxy inverso, dominios y certificados SSL.

En esta plataforma, el proxy es el unico componente pensado para exponer puertos hacia el exterior. Los paneles administrativos y servicios internos se mantienen accesibles por redes Docker o tuneles SSH.

## Servicios incluidos

- `npm`: Nginx Proxy Manager para gestionar proxy hosts, certificados y redirecciones.
- `db`: MariaDB para persistencia interna de Nginx Proxy Manager.

## Estructura

```text
proxy/
|-- docker-compose.yml
|-- .env.example
|-- .gitignore
`-- README.md
```

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
docker compose down
```

## Puertos

- `80`: trafico HTTP publico.
- `443`: trafico HTTPS publico.
- `81`: panel de administracion, publicado solo en `127.0.0.1`.

## Acceso al panel

El panel de administracion no queda expuesto directamente a Internet. Para acceder desde otro equipo, usar tunel SSH:

```bash
ssh -L 81:127.0.0.1:81 usuario@servidor
```

Luego abrir:

```text
http://127.0.0.1:81
```

En una instalacion nueva, Nginx Proxy Manager solicita cambiar las credenciales iniciales del panel en el primer ingreso.

## Redes

- `proxy_internal_net`: red interna entre Nginx Proxy Manager y MariaDB.
- `proxy_n8n_net`: red externa de ejemplo para conectar el servicio `n8n` al proxy.

Si se agrega otro servicio al proxy, se debe crear o declarar su red externa correspondiente y conectarla al servicio `npm`.

## Persistencia

- `proxy_data`: configuracion de Nginx Proxy Manager.
- `proxy_letsencrypt`: certificados SSL.
- `proxy_mysql_data`: datos de MariaDB.

## Seguridad

- No versionar `.env`.
- No subir certificados, respaldos ni datos persistentes.
- Cambiar credenciales iniciales del panel en el primer acceso.
- Mantener el puerto `81` restringido a localhost o a una red administrativa.
- Revisar cuidadosamente los servicios antes de exponerlos mediante proxy.

## Limitaciones

Esta configuracion corresponde a una base de laboratorio/portafolio. Antes de usarla en un entorno productivo conviene revisar hardening, respaldos, rotacion de certificados, politicas de acceso y actualizaciones controladas.
