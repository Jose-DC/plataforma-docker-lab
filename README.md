# Plataforma centralizada de entornos con Docker

Repositorio de portafolio basado en un prototipo desarrollado durante una practica profesional. El objetivo fue centralizar servicios de apoyo para levantar, administrar, monitorear y proteger entornos Docker de forma mas ordenada y reproducible.

El proyecto no se presenta como una plataforma productiva terminada, sino como una primera version funcional/laboratorio orientada a infraestructura, automatizacion, monitoreo y operacion de servicios.

## Problema que aborda

En entornos pequenos de laboratorio, desarrollo o apoyo operativo, levantar
servicios Docker de forma manual suele repetir pasos sensibles: preparar
variables, crear redes, publicar servicios, revisar logs, exponer paneles y
mantener documentacion minima. Cuando cada stack se arma de forma distinta, se
vuelve mas dificil diagnosticar, replicar o mantener el entorno.

Este proyecto propone una base ordenada para centralizar esas tareas: proxy,
gestion visual, monitoreo, escaneo de imagenes y generacion de stacks desde
plantillas reutilizables.

## Que resuelve

- Reduce repeticion al crear nuevos servicios Docker.
- Separa redes internas de redes de exposicion hacia el proxy inverso.
- Mantiene paneles administrativos ligados a localhost y acceso por tunel SSH.
- Agrega monitoreo base para host y contenedores.
- Incorpora revision inicial de imagenes con Trivy.
- Documenta limites, riesgos y pasos de operacion para no depender solo de
  conocimiento informal.

## Modos de uso

### Validacion local

En un equipo local, el proyecto sirve para comprobar que las plantillas,
redes, contenedores, variables y scripts funcionan correctamente. En este modo,
los servicios de aplicacion no publican puertos directamente al host; quedan
expuestos dentro de Docker y pueden conectarse al proxy por red interna.

Nginx Proxy Manager puede levantarse localmente para validar la conexion entre
contenedores, pero no reemplaza la configuracion real de dominio, DNS, IP
publica y certificados.

### Servidor con IP publica o dominio

El flujo completo con Nginx Proxy Manager esta pensado principalmente para un
servidor Linux: el proxy publica `80/443`, los servicios quedan en redes Docker
privadas y cada dominio/certificado se configura manualmente desde el panel.

En este modo el generador puede crear el entorno, crear la red externa,
registrarla en el compose del proxy, levantar el stack y conectar el proxy a la
red del proyecto.

## Alcance

- Administracion visual de contenedores con Portainer.
- Proxy inverso con Nginx Proxy Manager para exponer servicios mediante dominios y SSL.
- Monitoreo con Prometheus, Grafana, cAdvisor, Node Exporter y Alertmanager.
- Escaneo de imagenes locales con Trivy.
- Automatizacion con Python para generar estructuras base de nuevos stacks.
- Separacion de redes, volumenes y variables por servicio/proyecto.

## Validacion tecnica

La validacion local esta documentada en
[`docs/validacion-tecnica.md`](docs/validacion-tecnica.md). Hasta ahora se
comprobo la generacion de las 15 plantillas, la sintaxis del generador Python,
la validez de los archivos Docker Compose generados y pruebas de runtime con
Docker Desktop/WSL para los modulos principales.

Tambien se probo el flujo completo del generador con una plantilla
`static_nginx`, incluyendo creacion de red externa, registro en el proxy,
inicio del stack y conexion del contenedor de Nginx Proxy Manager a la red del
proyecto.

## Estructura del repositorio

```text
plataforma-docker/
|-- automatizacion/   # Script y plantillas para crear nuevos stacks
|-- monitoring/       # Prometheus, Grafana, cAdvisor, Node Exporter y Alertmanager
|-- n8n/              # Ejemplo de servicio n8n con PostgreSQL
|-- portainer/        # Portainer CE para gestion visual de contenedores
|-- proxy/            # Nginx Proxy Manager y base de datos
|-- security-trivy/   # Escaneo de imagenes Docker con Trivy
|-- docs/             # Validacion local y notas de publicacion
|-- .gitignore
`-- README.md
```

## Arquitectura general

```text
Usuario/Admin
    |
    | Tunel SSH para paneles administrativos
    v
Servidor Linux con Docker
    |
    |-- Proxy inverso: Nginx Proxy Manager
    |-- Gestion: Portainer CE
    |-- Monitoreo: Prometheus + Grafana + Alertmanager
    |-- Seguridad: Trivy
    |-- Automatizacion: Python + plantillas Docker Compose
    `-- Servicios/proyectos desplegados como stacks independientes
```

## Flujo esperado

1. Crear un nuevo stack desde una plantilla o de forma manual.
2. Definir variables locales en `.env` a partir de `.env.example`.
3. Levantar el servicio con Docker Compose.
4. Conectar el servicio al proxy inverso cuando corresponda.
5. Monitorear estado, logs y metricas.
6. Ejecutar revisiones de seguridad sobre imagenes Docker.

## Accesos administrativos

Los paneles administrativos se dejan ligados a `127.0.0.1` y se acceden mediante tunel SSH.

```bash
ssh -L 9443:127.0.0.1:9443 usuario@servidor    # Portainer
ssh -L 3000:127.0.0.1:3000 usuario@servidor    # Grafana
ssh -L 9090:127.0.0.1:9090 usuario@servidor    # Prometheus
ssh -L 9093:127.0.0.1:9093 usuario@servidor    # Alertmanager
ssh -L 81:127.0.0.1:81 usuario@servidor        # Nginx Proxy Manager
```

## Seguridad y versionado

- No subir archivos `.env` con credenciales reales.
- No versionar claves, tokens, certificados privados, respaldos ni datos persistentes.
- Mantener `.env.example` solo con valores de ejemplo.
- Revisar configuraciones antes de exponer servicios mediante proxy.
- Validar el uso de `/var/run/docker.sock`, ya que entrega control sobre el motor Docker del host.
- Publicar imagenes o capturas solo si no muestran dominios internos, IPs reales,
  usuarios, rutas privadas ni datos operacionales sensibles.

## Modulos

### `portainer/`

Panel local para administracion de contenedores, volumenes, redes, imagenes y stacks.

### `monitoring/`

Stack de observabilidad con Prometheus, Grafana, cAdvisor, Node Exporter y Alertmanager. Permite revisar metricas del host, contenedores y alertas basicas.

### `proxy/`

Proxy inverso basado en Nginx Proxy Manager. Centraliza dominios, certificados y publicacion de servicios.

### `security-trivy/`

Modulo para escanear imagenes Docker locales con Trivy y generar reportes de vulnerabilidades.

### `automatizacion/`

Script y plantillas para crear estructuras base de nuevos proyectos Docker de manera mas rapida.

### `n8n/`

Ejemplo de servicio desplegable dentro de la plataforma, con PostgreSQL y conexion esperada mediante proxy inverso.

## Estado del proyecto

Repositorio preparado como proyecto de portafolio. El alcance real es un
prototipo/laboratorio funcional sobre un unico host Docker, no una plataforma
productiva terminada. Para publicarlo en GitHub se recomienda seguir la guia
[`docs/publicacion-github.md`](docs/publicacion-github.md).
