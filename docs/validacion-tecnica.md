# Validacion tecnica local

Este documento resume las pruebas realizadas para preparar el repositorio como
proyecto de portafolio. La validacion separa lo que puede comprobarse sin
levantar contenedores de lo que requiere Docker Desktop o un host Linux con
Docker activo.

## Entorno revisado

- Windows con WSL2 Ubuntu 22.04.
- `make` disponible en WSL.
- `python3` disponible en WSL.
- Docker CLI instalado en Windows.
- Docker Desktop activo con integracion WSL.

## Nota sobre Docker Desktop en WSL

Durante la prueba inicial, Docker en WSL intento usar
`docker-credential-desktop.exe` y no lo encontro en el `PATH`. Para no modificar
la configuracion global del usuario, las pruebas de runtime se ejecutaron con
un `DOCKER_CONFIG` temporal vacio.

Este punto corresponde a configuracion local de Docker Desktop/WSL, no al
codigo del proyecto.

## Pruebas realizadas sin daemon Docker

### Catalogo de plantillas

Comando:

```bash
make -C automatizacion stacks
```

Resultado:

- Se listaron 15 plantillas disponibles.
- Las plantillas cubren FastAPI, Flask, Node, PHP, Laravel, Moodle,
  LimeSurvey, WordPress, Nginx estatico, MySQL y PostgreSQL.

### Sintaxis del generador

Comando:

```bash
python3 -m py_compile automatizacion/crearStack.py
```

Resultado:

- El archivo Python compila correctamente.

### Generacion de proyectos

Comando base:

```bash
PROJECTS_BASE_DIR=/tmp/plataforma-docker-iie \
python3 automatizacion/crearStack.py \
  -n demo_fastapi_validacion \
  -s FastAPI+postgres \
  --lang 3.12 \
  --dbv 16 \
  --solo-generar
```

Resultado:

- El generador copia la plantilla seleccionada.
- Reemplaza `${PROJECT}` por el nombre del proyecto.
- Crea un archivo `.env` local desde `.env.example`.
- No crea redes ni levanta contenedores cuando se usa `--solo-generar`.

### Validacion del catalogo completo

Se ejecuto el flujo `--solo-generar` para las 15 plantillas.

Resultado:

- 15 de 15 plantillas se generaron correctamente.

### Validacion de Docker Compose

Se valido `docker compose config` sobre:

- `monitoring/docker-compose.yml`
- `portainer/docker-compose.yml`
- `proxy/docker-compose.yml`
- `security-trivy/docker-compose.yml`
- `n8n/docker-compose.yml` usando una copia local de `.env.example` como `.env`
- plantillas generadas con `${PROJECT}` ya reemplazado

Resultado:

- Los modulos principales validan correctamente.
- Las 15 plantillas generadas validan correctamente.
- Las plantillas crudas no deben validarse directamente, porque usan
  `${PROJECT}` en nombres de redes y volumenes. Primero deben generarse con el
  script.

## Ajustes realizados durante la revision

- Se corrigieron comentarios corruptos en las plantillas `php+mysql` y
  `php+postgres` que provocaban error de parser YAML.
- Se quito el uso obligatorio de TTY en `make crear`, porque el generador no
  requiere interaccion y debe poder ejecutarse tambien desde scripts o CI.
- Se documento la necesidad de crear la red externa `proxy_n8n_net` antes de
  levantar `proxy` o `n8n`.

## Pruebas realizadas con Docker activo

### Stack generado `static_nginx`

Flujo probado:

```bash
docker network create proxy_demo_static_net
PROJECTS_BASE_DIR=/tmp/plataforma-docker-iie-runtime \
python3 automatizacion/crearStack.py \
  -n demo_static \
  -s static_nginx \
  --solo-generar

cd demo_static
docker compose config --quiet
docker compose up -d
docker compose ps
```

Resultado:

- El contenedor `demo_static_app` quedo en estado `running`.
- El servicio no publico puertos al host; solo expuso el puerto 80 dentro de la
  red Docker.
- La prueba se limpio eliminando contenedor y red temporal.

### Monitoring

Flujo probado:

```bash
cd monitoring
docker compose config --quiet
docker compose up -d
docker compose ps
```

Resultado:

- `infra_prometheus`: `running`.
- `infra_grafana`: `running` y `healthy`.
- `infra_alertmanager`: `running` y `healthy`.
- `infra_cadvisor`: `running` y `healthy`.
- `infra_node_exporter`: `running`.
- Los puertos administrativos quedaron ligados a `127.0.0.1`.
- La prueba se limpio con `docker compose down -v`.

### Portainer

Flujo probado:

```bash
cd portainer
docker compose config --quiet
docker compose up -d
docker compose ps
```

Resultado:

- `portainer_app` quedo en estado `running`.
- El panel quedo publicado en `127.0.0.1:9443`.
- La prueba se limpio con `docker compose down -v`.

### Generador mediante Makefile

Flujo probado:

```bash
cd automatizacion
make build
make crear nombre=demo_static_make stack=static_nginx solo_generar=1
```

Resultado:

- La imagen `stackgen:1.0` se construyo correctamente.
- `make crear` genero el stack `demo_static_make`.
- El `docker-compose.yml` generado valido con `docker compose config --quiet`.

### Flujo completo con proxy local

Flujo probado en copia temporal:

```bash
cd proxy
cp .env.example .env
docker network create proxy_n8n_net
docker compose --env-file .env up -d

cd ../automatizacion
make build
make crear nombre=demo_static_full stack=static_nginx
```

Resultado:

- Nginx Proxy Manager levanto `infra_nginx_proxy` e `infra_nginx_db`.
- El generador creo el proyecto `demo_static_full`.
- Se creo la red externa `proxy_demo_static_full_net`.
- Se registro `proxy_demo_static_full_net` en el `docker-compose.yml` del proxy.
- Se levanto `demo_static_full_app`.
- El contenedor `infra_nginx_proxy` quedo conectado a
  `proxy_demo_static_full_net` junto al contenedor de la aplicacion.
- El proxy fue reiniciado por el script para aplicar la conexion.

La prueba valida la orquestacion local entre proxy y stack generado. La
publicacion real mediante dominio, DNS, IP publica y certificado SSL sigue
siendo una tarea propia de servidor.

### Trivy

Flujo probado:

```bash
cd security-trivy
docker compose --profile sec run --rm trivy version
```

Resultado:

- El contenedor de Trivy ejecuto correctamente.
- Version probada: `0.67.2`.

## Pruebas pendientes o recomendadas

Estas pruebas siguen siendo recomendables antes de publicar evidencia visual o
declarar el proyecto como completamente probado:

```bash
docker network create proxy_n8n_net
```

```bash
cd proxy
cp .env.example .env
docker compose up -d
docker compose ps
```

```bash
cd ../automatizacion
make build
make crear nombre=demo_static stack=static_nginx
```

Tambien falta probar un flujo completo con el proxy realmente activo:

- revisar acceso mediante proxy host;
- guardar capturas sin informacion sensible.

## Criterio de aceptacion

El proyecto puede presentarse como prototipo/laboratorio funcional cuando:

- Los modulos principales levantan sin errores.
- Los paneles administrativos quedan publicados solo en `127.0.0.1`.
- El generador crea al menos una plantilla y su compose valida.
- No existen `.env` reales, claves privadas, certificados o datos persistentes
  versionados.
- Se documentan las limitaciones: no es plataforma productiva, no reemplaza
  Kubernetes, no resuelve gobierno completo de secretos y requiere hardening
  antes de uso real.
