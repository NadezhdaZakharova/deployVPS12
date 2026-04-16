"""Загрузка data.sql в БД (SQLite и PostgreSQL). Запуск: python load_data.py"""
import os
import re
import sys

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.db import connection


def _sql_statements(sql_text: str) -> list[str]:
    lines = []
    for line in sql_text.splitlines():
        s = line.strip()
        if s.startswith("--"):
            continue
        lines.append(line)
    text = "\n".join(lines)
    parts = [p.strip() for p in re.split(r";\s*\n?", text) if p.strip()]
    return parts


def main() -> None:
    path = os.path.join(os.path.dirname(__file__), "data.sql")
    with open(path, encoding="utf-8") as f:
        sql = f.read()

    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM video_cards")
        if cursor.fetchone()[0] > 0:
            print("Данные уже есть, пропускаю.")
            return

    with connection.cursor() as cursor:
        for stmt in _sql_statements(sql):
            cursor.execute(stmt)
    print("Данные загружены.")


if __name__ == "__main__":
    main()
