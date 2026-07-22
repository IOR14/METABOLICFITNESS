#!/usr/bin/env bash
# Cron helper: sync BBB recordings → Supabase (run on VPS or any scheduler)
# Crontab example (every 20 min):
#   */20 * * * * /opt/metabolic/scripts/sync-bbb-recordings.sh >> /var/log/mf-bbb-sync.log 2>&1

set -euo pipefail

FUNCTIONS_URL="${FUNCTIONS_URL:-https://epvakbxseshjksfhoorl.supabase.co/functions/v1/live-sync-recordings}"
SYNC_CRON_SECRET="${SYNC_CRON_SECRET:?Define SYNC_CRON_SECRET}"

curl -fsS -X POST "$FUNCTIONS_URL" \
  -H "X-Sync-Secret: ${SYNC_CRON_SECRET}" \
  -H "Content-Type: application/json"

echo
echo "$(date -Is) sync OK"
