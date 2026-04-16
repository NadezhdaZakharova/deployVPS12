#!/usr/bin/env bash
# Запускать НА VPS из корня репозитория (там же, где docker-compose.prod.yml).
# Пример: cd /opt/shop && bash scripts/vps-on-server.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ ! -f docker-compose.prod.yml ]]; then
  echo "Ошибка: нет docker-compose.prod.yml в $ROOT"
  exit 1
fi

if command -v ufw >/dev/null 2>&1; then
  echo ">>> UFW: разрешаю 8080/tcp (нужен sudo)"
  sudo ufw allow 8080/tcp || true
  sudo ufw status || true
fi

echo ">>> Docker Compose (prod)"
docker compose -f docker-compose.prod.yml up --build -d
docker compose -f docker-compose.prod.yml ps

echo ">>> Проверка health на самом сервере"
curl -sS --max-time 10 http://127.0.0.1:8080/api/health && echo

echo "Готово. Снаружи проверь: curl http://<IP_СЕРВЕРА>:8080/api/health"
