"""Settings produksi: semua nilai sensitif dibaca dari environment.

Variabel yang wajib di-set di server:
  SECRET_KEY, DATABASE_URL, ALLOWED_HOSTS, CORS_ALLOWED_ORIGINS
"""
import os

import dj_database_url
from dotenv import load_dotenv

from .base import *  # noqa: F401,F403

# Memuat variabel dari file .env bila ada — supaya bisa menjalankan mode produksi
# secara lokal tanpa meng-export env manual. Di server sungguhan, env diisi lewat
# environment proses (systemd/PM2/Docker) dan file .env tidak perlu ada.
load_dotenv()

DEBUG = False

# Kunci rahasia dibaca dari environment — jangan pernah hardcode di repo.
SECRET_KEY = os.environ["SECRET_KEY"]

# Daftar host dipisah koma, contoh: "api.situskalian.com,localhost"
ALLOWED_HOSTS = [
    host.strip() for host in os.environ.get("ALLOWED_HOSTS", "").split(",") if host.strip()
]

# Koneksi PostgreSQL dari satu env var DATABASE_URL
# (format: postgres://user:password@host:port/nama_db)
DATABASES = {
    "default": dj_database_url.config(conn_max_age=600),
}

# Origin frontend yang diizinkan, dipisah koma —
# contoh: "https://situs-kalian.netlify.app,http://localhost:5173"
CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get("CORS_ALLOWED_ORIGINS", "").split(",")
    if origin.strip()
]
