#!/usr/bin/env bash
# Запускать из WSL из корня проекта (рядом с manage.py).
# Копирует файлы на VPS по rsync и перезапускает docker compose.
#
# Использование:
#   bash scripts/push-to-vps.sh root@81.90.182.174 /opt/shop
#
# Перед первым запуском на VPS один раз:
#   ssh root@81.90.182.174 "mkdir -p /opt/shop"
#
set -euo pipefail

REMOTE="${1:?Укажи: user@host   Пример: root@81.90.182.174}"
RDIR="${2:?Укажи: удалённый каталог   Пример: /opt/shop}"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if ! command -v rsync >/dev/null 2>&1; then
  echo "Установи rsync: sudo apt install -y rsync"
  exit 1
fi

echo ">>> rsync -> ${REMOTE}:${RDIR}/"
rsync -avz \
  --exclude '.venv/' \
  --exclude 'venv/' \
  --exclude '__pycache__/' \
  --exclude '*.pyc' \
  --exclude '.git/' \
  --exclude 'db.sqlite3' \
  --exclude 'media/' \
  --exclude '.cursor/' \
  ./ "${REMOTE}:${RDIR}/"

echo ">>> ssh: docker compose prod"
ssh "$REMOTE" "cd '$RDIR' && bash scripts/vps-on-server.sh"

echo ">>> С твоего ПК (WSL) проверь внешний IP:"
echo "    curl -sS --max-time 10 http://81.90.182.174:8080/api/health"
echo "    (подставь свой IP, если другой)"
