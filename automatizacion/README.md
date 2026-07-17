# Generador de entornos Docker

Este modulo corresponde a un prototipo desarrollado durante una practica
profesional. Su objetivo es reducir el trabajo manual necesario para crear un
entorno Docker desde una plantilla, conectarlo a la red del proxy inverso e
iniciar sus servicios.

No es una plataforma de aprovisionamiento para produccion. Es una primera
version funcional y reproducible que documenta decisiones de automatizacion,
redes y operacion con Docker Compose.

## Que resuelve

Este proyecto busca estandarizar la creacion de entornos Docker pequeños para
laboratorio y desarrollo. En lugar de copiar archivos manualmente, editar
variables una por una y conectar cada stack al proxy de forma repetitiva, el
flujo permite generar una base operativa desde plantillas reutilizables.

## Valor del proyecto

- Reduce tareas manuales repetitivas al crear nuevos entornos.
- Estandariza el uso de plantillas Docker Compose.
- Separa redes internas y redes de exposicion hacia el proxy.
- Genera configuracion local sin subir secretos reales al repositorio.
- Deja una base reutilizable para pruebas, laboratorios y documentacion.

## Que automatiza

1. Valida el nombre y la plantilla solicitada.
2. Copia la plantilla a un directorio de proyecto independiente.
3. Genera el archivo `.env` y reemplaza los valores configurables.
4. Crea contrasenas aleatorias cuando la plantilla usa marcadores `change-me`.
5. Crea una red externa dedicada para el proxy.
6. Registra esa red en el `docker-compose.yml` de Nginx Proxy Manager.
7. Inicia el stack y conecta el proxy.

La asociacion del dominio y el certificado TLS en Nginx Proxy Manager sigue
siendo un paso manual.

## Flujo resumido

```text
Seleccion de plantilla
-> copia del stack base
-> generacion de .env
-> creacion de red externa
-> registro en el proxy
-> despliegue con Docker Compose
```

## Tecnologias involucradas

- Python
- Docker
- Docker Compose
- GNU Make
- Nginx Proxy Manager
- YAML
- Variables de entorno y secretos locales

## Estructura

```text
automatizacion/
|-- crearStack.py
|-- Dockerfile
|-- Makefile
|-- requirements.txt
`-- templates/
```

Cada plantilla incluye, como minimo, un archivo `docker-compose.yml` y un
`.env.example`. Algunas incorporan una aplicacion minima para comprobar la
conexion con la base de datos; otras utilizan una imagen preconstruida.

## Requisitos

- Linux
- Docker Engine con el plugin Docker Compose
- GNU Make
- Nginx Proxy Manager iniciado desde `../proxy`
- Permiso para acceder a `/var/run/docker.sock`

El acceso al socket de Docker entrega privilegios elevados sobre el host. La
imagen debe utilizarse solo en un equipo administrado y con plantillas
confiables.

## Uso

Construir el generador:

```bash
cd /srv/proyectosDocker/automatizacion
make build
```

Listar las plantillas detectadas:

```bash
make stacks
```

Crear e iniciar un entorno:

```bash
make crear nombre=demo_api stack=FastAPI+postgres lang=3.12 dbv=16
```

Generar los archivos sin crear redes ni iniciar contenedores:

```bash
make crear nombre=demo_api stack=FastAPI+postgres solo_generar=1
```

`lang` y `dbv` son opcionales. Solo modifican plantillas que declaran
`LANG_VERSION` o `DB_VERSION`.

## Convenciones

- `nombre`: minusculas, numeros, guion o guion bajo; maximo 63 caracteres.
- `.env.example`: valores publicos y marcadores, nunca secretos reales.
- `.env`: archivo generado localmente y excluido de Git.
- `proxy_<proyecto>_net`: red externa compartida por la aplicacion y el proxy.
- `<proyecto>_internal_net`: red interna de los servicios del stack.

La ruta base predeterminada es `/srv/proyectosDocker`. Para ejecutar el script
fuera del contenedor puede cambiarse mediante `PROJECTS_BASE_DIR`.

## Alcance real

Este modulo automatiza la preparacion de stacks sobre un unico host Docker y
sirve como base de laboratorio. No reemplaza una plataforma de orquestacion, no
incluye gobernanza completa de secretos y no resuelve por si solo la operacion
productiva del servicio publicado.

## Plantillas incluidas

El prototipo conserva combinaciones de PHP, Laravel, Node.js, Flask, FastAPI,
WordPress, Moodle, LimeSurvey, Nginx, MySQL y PostgreSQL. No todas representan
aplicaciones completas: son bases de despliegue para validar la generacion del
entorno, las redes y la comunicacion entre servicios.

Consulta el [catalogo de plantillas](templates/README.md) para comparar los
servicios y paneles opcionales disponibles.

## Limitaciones conocidas

- El flujo modifica el Compose del proxy para conservar las conexiones de red.
- No existe rollback automatico si Docker falla durante el despliegue.
- Las plantillas requieren pruebas periodicas frente a nuevas versiones de sus
  imagenes.
- El dominio y el certificado TLS se configuran manualmente.
- El generador esta orientado a un unico host Docker, no a un cluster.

## Lo que conviene revisar al probarlo

- Que `make stacks` detecte las plantillas disponibles.
- Que `make crear ... solo_generar=1` genere un directorio nuevo con su `.env`.
- Que `docker compose config` valide la plantilla generada sin errores.
- Que la red `proxy_<proyecto>_net` exista cuando se usa el flujo completo.
- Que el stack quede listo para asociarse manualmente a un dominio en el proxy.
