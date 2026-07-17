# Catalogo de plantillas

Estas plantillas generan entornos reproducibles para desarrollo y laboratorio
en un unico host Docker. No representan arquitecturas productivas ni buscan
reemplazar una plataforma completa de provisionamiento.

## Que muestran

- Bases reutilizables para levantar servicios con Docker Compose.
- Integracion entre aplicacion, base de datos y panel opcional.
- Uso de variables de entorno y redes separadas por proyecto.
- Un punto de partida rapido para pruebas tecnicas y documentacion.

## Plantillas disponibles

| Plantilla | Aplicacion | Base de datos | Panel opcional |
| --- | --- | --- | --- |
| `FastAPI+mysql` | FastAPI | MySQL | phpMyAdmin |
| `FastAPI+postgres` | FastAPI | PostgreSQL | pgAdmin |
| `laravel+mysql` | Laravel | MySQL | phpMyAdmin |
| `laravel+postgres` | Laravel | PostgreSQL | pgAdmin |
| `limesurvey+mysql` | LimeSurvey | MySQL | phpMyAdmin |
| `moodle+mysql` | Moodle | MySQL | phpMyAdmin |
| `moodle+postgres` | Moodle | PostgreSQL | pgAdmin |
| `node+mysql` | Node.js | MySQL | phpMyAdmin |
| `node+postgres` | Node.js | PostgreSQL | pgAdmin |
| `php+mysql` | PHP | MySQL | phpMyAdmin |
| `php+postgres` | PHP | PostgreSQL | pgAdmin |
| `python-flask+mysql` | Flask | MySQL | phpMyAdmin |
| `python-flask+postgres` | Flask | PostgreSQL | pgAdmin |
| `static_nginx` | Sitio estatico | No utiliza | No utiliza |
| `wordpress+mysql` | WordPress | MySQL | phpMyAdmin |

## Flujo comun

1. `crearStack.py` copia la plantilla seleccionada.
2. Genera `.env` con nombre, versiones y secretos locales.
3. Prepara las redes del proyecto.
4. Levanta los servicios definidos en Docker Compose.
5. Deja el stack listo para conectarlo al proxy inverso.

Ejemplo:

```bash
cd /srv/proyectosDocker/automatizacion
make crear nombre=demo_api stack=FastAPI+postgres lang=3.12 dbv=16
```

## Cuando usar este catalogo

Este directorio sirve para entender rapidamente que tipos de stack puede crear
el proyecto y con que combinaciones trabaja. Cada plantilla tiene su propio
README con notas breves de uso, validacion y alcance.

## Alcance

Las plantillas permiten comprobar imagenes, redes, persistencia y comunicacion
entre servicios. No incluyen por defecto alta disponibilidad, respaldo,
rotacion de secretos, CI/CD, observabilidad completa ni endurecimiento para
Internet.
