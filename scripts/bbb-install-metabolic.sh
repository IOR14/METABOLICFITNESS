#!/usr/bin/env bash
# Wrapper de instalación BBB 3.0 para Metabolic Fitness
# Uso (como root en Ubuntu 22.04):
#   chmod +x scripts/bbb-install-metabolic.sh
#   ./scripts/bbb-install-metabolic.sh
#
# Variables opcionales:
#   BBB_HOST=live.metabolicfitness.cl
#   BBB_EMAIL=director@whitesoultech.cl

set -euo pipefail

BBB_HOST="${BBB_HOST:-live.metabolicfitness.cl}"
BBB_EMAIL="${BBB_EMAIL:-director@whitesoultech.cl}"

echo "==> Metabolic Fitness — instalando BigBlueButton 3.0"
echo "    Host:  $BBB_HOST"
echo "    Email: $BBB_EMAIL"
echo

if [[ "$(id -u)" -ne 0 ]]; then
  echo "ERROR: ejecuta este script como root (sudo -i)."
  exit 1
fi

if ! grep -qi 'ubuntu' /etc/os-release 2>/dev/null; then
  echo "ADVERTENCIA: se recomienda Ubuntu 22.04 limpio."
fi

echo "==> Comprobando DNS de $BBB_HOST ..."
if ! getent hosts "$BBB_HOST" >/dev/null 2>&1; then
  echo "ERROR: $BBB_HOST no resuelve. Configura el registro A antes de instalar."
  exit 1
fi

echo "==> Ejecutando bbb-install.sh (esto puede tardar 15–40 min)..."
wget -qO- https://raw.githubusercontent.com/bigbluebutton/bbb-install/v3.0.x-release/bbb-install.sh \
  | bash -s -- -w -v jammy-300 -s "$BBB_HOST" -e "$BBB_EMAIL"

echo
echo "==> Estado del servidor:"
bbb-conf --check || true

echo
echo "==> Credenciales API (guarda BBB_URL y BBB_SECRET en Supabase secrets / .env):"
bbb-conf --secret

echo
echo "==> Listo. Siguiente: schema_live.sql + Edge Functions (ver docs/bbb-install.md)"
