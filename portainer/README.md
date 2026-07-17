# Portainer - Gestion de contenedores

Este modulo levanta Portainer CE como panel local para administrar contenedores, volumenes, imagenes, redes y stacks Docker dentro de la plataforma.

El panel no queda expuesto directamente a Internet. El acceso se limita a `127.0.0.1` y se recomienda entrar mediante tunel SSH cuando se administra desde otro equipo.

## Que permite revisar

- Contenedores y stacks activos.
- Estado general de servicios.
- Logs de contenedores.
- Imagenes, volumenes y redes Docker.
- Recursos que pueden quedar en desuso despues de pruebas o actualizaciones.

## Estructura

```text
portainer/
|-- docker-compose.yml   # Stack de Portainer CE
```

## Uso basico

Desde la carpeta `portainer/`:

```bash
docker compose up -d
docker compose ps
docker compose down
```

## Acceso

Portainer queda publicado solo en localhost:

```text
https://127.0.0.1:9443
```

Ejemplo de tunel SSH desde un equipo administrador:

```bash
ssh -L 9443:127.0.0.1:9443 usuario@servidor
```

Luego abrir en el navegador:

```text
https://127.0.0.1:9443
```

## Persistencia

El volumen `portainer_data` almacena configuracion, usuarios y datos internos del panel.

## Consideraciones de seguridad

- El contenedor monta `/var/run/docker.sock`, por lo que Portainer puede administrar el motor Docker del host.
- El acceso al panel debe restringirse a administradores.
- No se deben publicar credenciales ni respaldos del volumen `portainer_data`.
- Para acciones destructivas, como borrar volumenes, conviene validar primero el impacto sobre los servicios.

## Rol dentro de la plataforma

Portainer se usa como apoyo operativo para revisar y administrar el entorno Docker. No reemplaza la documentacion tecnica ni los procedimientos de despliegue, pero facilita tareas de diagnostico, revision de logs y control visual del estado de los contenedores.
