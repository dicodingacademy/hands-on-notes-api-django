#!/usr/bin/env python
"""Utilitas baris perintah Django. Saat pengembangan memakai settings dev (SQLite)."""
import os
import sys


def main():
    # Default ke settings dev — di server produksi, gunicorn memakai settings prod.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.dev")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Tidak bisa mengimpor Django. Pastikan sudah terpasang dan "
            "virtual environment sudah aktif."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
