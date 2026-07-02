"""Settings pengembangan: DEBUG aktif, database SQLite.

SQLite dipilih agar `python manage.py test` dan percobaan lokal
berjalan tanpa perlu PostgreSQL (termasuk di CI).
"""
from dotenv import load_dotenv

from .base import *  # noqa: F401,F403
from .base import BASE_DIR

# Memuat variabel dari file .env bila ada — supaya konfigurasi opsional seperti
# AI_SERVICE_URL tersedia saat pengembangan lokal tanpa perlu meng-export manual.
# SECRET_KEY & database dev tetap hardcoded di bawah (tidak bergantung pada .env).
load_dotenv()

DEBUG = True

# Kunci ini hanya untuk pengembangan lokal — produksi memakai env SECRET_KEY.
SECRET_KEY = "django-insecure-kunci-khusus-pengembangan"

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Origin frontend saat pengembangan lokal (Vite)
CORS_ALLOWED_ORIGINS = ["http://localhost:5173"]
