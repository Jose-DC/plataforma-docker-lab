# Monitoring - Prometheus, Grafana y Alertmanager

Este modulo levanta un stack basico de monitoreo para revisar metricas del servidor y contenedores Docker. Esta pensado como apoyo operativo para diagnostico, revision de consumo de recursos y alertas iniciales.

Los paneles quedan publicados solo en `127.0.0.1`, por lo que el acceso recomendado es mediante tunel SSH.

## Servicios incluidos

- `prometheus`: recoleccion y consulta de metricas.
- `grafana`: visualizacion mediante dashboards.
- `cadvisor`: metricas de contenedores Docker.
- `node-exporter`: metricas del host Linux.
- `alertmanager`: recepcion y gestion de alertas generadas por Prometheus.

## Estructura

```text
monitoring/
|-- alertmanager/
|   `-- alertmanager.yml
|-- dashboards/
|   `-- dashboard_Grafana.json
|-- prometheus/
|   |-- alert_rules.yml
|   `-- prometheus.yml
|-- docker-compose.yml
`-- README.md
```

## Uso basico

Desde la carpeta `monitoring/`:

```bash
docker compose up -d
docker compose ps
docker compose down
```

Levantar solo un servicio:

```bash
docker compose up -d grafana
docker compose up -d prometheus
```

## Acceso por tunel SSH

```bash
ssh -L 3000:127.0.0.1:3000 usuario@servidor    # Grafana
ssh -L 9090:127.0.0.1:9090 usuario@servidor    # Prometheus
ssh -L 9093:127.0.0.1:9093 usuario@servidor    # Alertmanager
```

Luego abrir en el navegador:

```text
http://127.0.0.1:3000
http://127.0.0.1:9090
http://127.0.0.1:9093
```

## Alertas

Las reglas se encuentran en `prometheus/alert_rules.yml` e incluyen ejemplos para:

- CPU elevada del host.
- RAM elevada del host.
- Disco con alto uso.
- cAdvisor sin metricas.
- Contenedores con CPU/RAM elevada.
- Contenedores con reinicios frecuentes.
- Contenedores que dejan de reportar metricas.

Alertmanager queda con un receptor local de ejemplo. No se versionan correos, claves SMTP ni tokens. Si se quiere enviar alertas por correo, Slack u otro canal, se debe configurar en una copia local no publica.

## Persistencia

- `monitoring_grafana_data`: datos de Grafana.
- `infra_prometheus_data`: metricas historicas de Prometheus.
- `monitoring_alertmanager_data`: estado interno de Alertmanager.

## Consideraciones

- El stack es util para laboratorio y apoyo operativo, no reemplaza una solucion de observabilidad completa.
- Los umbrales de alerta deben ajustarse segun recursos reales del servidor.
- Los dashboards exportados pueden usarse como base, pero conviene revisarlos antes de reutilizarlos en otro entorno.
- Para recargar reglas de Prometheus se puede reiniciar el servicio o usar el endpoint de recarga si esta habilitado.
