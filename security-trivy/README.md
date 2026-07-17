# Security Trivy - Escaneo de imagenes Docker

Este modulo agrega una capa basica de revision de seguridad para la plataforma Docker. Su objetivo es escanear imagenes locales con Trivy, generar reportes en formatos legibles y conservar un historial reducido para revision posterior.

No expone servicios ni puertos. Se ejecuta de forma manual o programada desde el host donde esta instalada la plataforma.

## Que hace

- Lista las imagenes Docker disponibles en el host.
- Ejecuta Trivy contra cada imagen local.
- Genera reportes en formato JSON y TXT.
- Guarda los resultados en carpetas por fecha.
- Registra la ejecucion en `logs/scan.log`.
- Conserva solo los ultimos 3 grupos de reportes para evitar crecimiento innecesario.

## Estructura

```text
security-trivy/
|-- docker-compose.yml   # Servicio Trivy ejecutado bajo perfil sec
|-- trivy.yaml           # Configuracion base del escaneo
|-- .trivyignore         # Exclusiones justificadas, vacio por defecto
|-- scan-all.sh          # Script de escaneo masivo y rotacion
|-- reports/             # Reportes generados (ignorado por Git)
|-- logs/                # Logs de ejecucion (ignorado por Git)
\-- trivy-cache/         # Cache local de Trivy (ignorado por Git)
```

## Uso manual

Desde la carpeta `security-trivy/`:

```bash
chmod +x scan-all.sh
./scan-all.sh
```

El script usa por defecto la carpeta donde se encuentra. Si se despliega en otra ruta, se puede indicar explicitamente:

```bash
TRIVY_BASE_DIR=/srv/proyectosDocker/security-trivy ./scan-all.sh
```

## Escaneo de una imagen puntual

```bash
docker compose --profile sec run --rm trivy \
  image --config /work/trivy.yaml \
  --ignorefile /root/.trivyignore \
  nombre-imagen:tag
```

## Reportes

Cada ejecucion crea una carpeta con fecha en:

```text
reports/YYYY-MM-DD_HH-MM-SS/
```

Archivos generados:

- `.json`: salida completa para revision tecnica o procesamiento posterior.
- `.txt`: salida en tabla para lectura rapida.

## Automatizacion sugerida

Ejemplo de cron diario a las 03:30:

```cron
30 3 * * * /srv/proyectosDocker/security-trivy/scan-all.sh
```

La automatizacion debe ajustarse a la ruta real del servidor.

## Criterio de exclusiones

El archivo `.trivyignore` queda vacio por defecto. Si se agrega una CVE, debe existir una justificacion tecnica: falso positivo, vulnerabilidad no accionable en una imagen de tercero, aceptacion temporal del riesgo o correccion pendiente del mantenedor.

## Limitaciones

- El escaneo identifica vulnerabilidades conocidas, pero no reemplaza hardening, revision de secretos ni control de configuracion.
- Los hallazgos deben revisarse manualmente antes de tomar decisiones.
- Algunas vulnerabilidades pueden depender del mantenedor de una imagen base.
- Esta configuracion esta pensada como apoyo operativo para un laboratorio/plataforma Docker, no como un sistema completo de gestion de vulnerabilidades.
