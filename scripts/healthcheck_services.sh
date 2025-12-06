#!/usr/bin/env bash

# Lista de serviços críticos da plataforma de ingressos
SERVICES=(
  "Checkout API|https://api.ingresse.local/health/checkout"
  "Ticketing API|https://api.ingresse.local/health/ticketing"
  "Notifications API|https://api.ingresse.local/health/notifications"
)

LOG_FILE="../data/healthchecks.log"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

mkdir -p "$(dirname "$LOG_FILE")"

echo "[$TIMESTAMP] Iniciando healthcheck dos serviços..." | tee -a "$LOG_FILE"

for service in "${SERVICES[@]}"; do
  NAME="${service%%|*}"
  URL="${service##*|}"

  # Faz apenas uma requisição HEAD para testar disponibilidade
  HTTP_CODE=$(curl -o /dev/null -s -w "%{http_code}" "$URL")

  if [ "$HTTP_CODE" -eq 200 ]; then
    STATUS="OK"
  else
    STATUS="CRITICAL"
  fi

  echo "[$TIMESTAMP] $NAME - $URL - HTTP $HTTP_CODE - $STATUS" | tee -a "$LOG_FILE"
done
