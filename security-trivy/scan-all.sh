#!/bin/bash
# Escaneo masivo con Trivy y rotacion de reportes.
set -euo pipefail

# Entorno basico para ejecucion manual o por cron.
export SHELL=/bin/bash
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Por defecto usa la carpeta donde vive este script. En servidor se puede
# sobreescribir con TRIVY_BASE_DIR=/srv/proyectosDocker/security-trivy.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="${TRIVY_BASE_DIR:-$SCRIPT_DIR}"
REPORTS_DIR="$BASE_DIR/reports"
LOGS_DIR="$BASE_DIR/logs"
DATE_DIR="$(date +%F_%H-%M-%S)"
HOST_OUT_DIR="$REPORTS_DIR/$DATE_DIR"
CONTAINER_OUT_DIR="/reports/$DATE_DIR"
DOCKER="${DOCKER_BIN:-docker}"
COMPOSE_FILE="$BASE_DIR/docker-compose.yml"

mkdir -p "$HOST_OUT_DIR" "$LOGS_DIR"
LOG_FILE="$LOGS_DIR/scan.log"

exec > >(tee -a "$LOG_FILE") 2>&1

cd "$BASE_DIR"

echo "[$(date '+%F %T')] Iniciando escaneo. Carpeta: $HOST_OUT_DIR"

IMAGES=$("$DOCKER" images --format '{{.Repository}}:{{.Tag}}' | grep -v '<none>' || true)

if [ -z "$IMAGES" ]; then
  echo "[$(date '+%F %T')] No hay imagenes locales para escanear."
else
  for IMG in $IMAGES; do
    # Se omiten imagenes auxiliares del propio stack de seguridad/monitoreo.
    if [[ "$IMG" =~ ^aquasec/trivy ]] || \
       [[ "$IMG" == "gcr.io/cadvisor/cadvisor:latest" ]] || \
       [[ "$IMG" == "prom/node-exporter:latest" ]]; then
      echo "[$(date '+%F %T')] -> Saltando $IMG (imagen auxiliar)"
      continue
    fi

    SAFE_NAME=$(echo "$IMG" | tr '/:' '__')
    echo "[$(date '+%F %T')] -> Escaneando $IMG"

    "$DOCKER" compose -f "$COMPOSE_FILE" --profile sec run --rm trivy \
      image --config /work/trivy.yaml \
      --ignorefile /root/.trivyignore \
      --scanners vuln \
      --format json \
      --output "$CONTAINER_OUT_DIR/${SAFE_NAME}.json" \
      "$IMG" || true

    "$DOCKER" compose -f "$COMPOSE_FILE" --profile sec run --rm trivy \
      image --config /work/trivy.yaml \
      --ignorefile /root/.trivyignore \
      --scanners vuln \
      --format table \
      --output "$CONTAINER_OUT_DIR/${SAFE_NAME}.txt" \
      "$IMG" || true
  done
fi

echo "[$(date '+%F %T')] Reportes guardados en $HOST_OUT_DIR"

cd "$REPORTS_DIR"
KEPT=$(ls -dt */ 2>/dev/null | head -n 3 | tr '\n' ' ' || true)
DELETED=$(ls -dt */ 2>/dev/null | tail -n +4 || true)

if [ -n "$DELETED" ]; then
  echo "[$(date '+%F %T')] Rotacion: se eliminan carpetas antiguas:"
  echo "$DELETED"
  echo "$DELETED" | xargs -r rm -rf
else
  echo "[$(date '+%F %T')] Rotacion: no hay carpetas antiguas que eliminar."
fi

echo "[$(date '+%F %T')] Se conservan (max 3): $KEPT" | sed 's/ \+$//'
echo "[$(date '+%F %T')] Escaneo finalizado."
