# Publicacion en GitHub

Guia corta para preparar este repositorio como proyecto publico de portafolio.

## Repositorio recomendado

Crear un repositorio independiente en la cuenta `Jose-DC`.

Nombre sugerido:

```text
plataforma-docker-lab
```

Alternativa si se quiere conservar el nombre original:

```text
plataforma-docker-IIE
```

El proyecto debe vivir como repositorio propio. El portafolio web solo deberia
enlazarlo y mostrar una ficha resumida con evidencias sanitizadas.

## Antes de publicar

- Revisar que no existan archivos `.env` reales.
- Revisar que no existan claves, certificados, dumps, respaldos ni datos de
  servicios.
- No publicar capturas que muestren dominios internos, IPs reales, usuarios,
  rutas de servidor o informacion operacional privada.
- Mantener solo `.env.example` con valores de ejemplo.
- Confirmar que los proyectos generados de prueba no queden versionados.
- Confirmar que `docker compose config --quiet` valida los modulos principales.

## Comandos sugeridos

Desde la raiz del proyecto:

```bash
git status --short
git add -A
git commit -m "Prepare Docker platform lab for portfolio publication"
git branch -M main
git remote set-url origin https://github.com/Jose-DC/plataforma-docker-lab.git
git push -u origin main
```

Si el repositorio remoto aun no existe, primero crearlo vacio en GitHub y luego
ejecutar el `git push`.

## Enlace desde el portafolio

La ficha del portafolio deberia incluir:

- Problema que resuelve.
- Arquitectura general.
- Tecnologias usadas.
- Pruebas realizadas.
- Limitaciones conocidas.
- Link al repositorio.
- Imagenes o diagramas sin informacion sensible.
