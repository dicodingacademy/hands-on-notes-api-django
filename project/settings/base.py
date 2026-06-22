"""Settings dasar yang dipakai bersama oleh dev.py dan prod.py."""
from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "corsheaders",
    "rest_framework",
    "notes",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # CORS harus berada sebelum CommonMiddleware agar header
    # Access-Control-Allow-Origin ikut terkirim di semua respons.
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "project.urls"
WSGI_APPLICATION = "project.wsgi.application"

REST_FRAMEWORK = {
    # Autentikasi memakai JWT di header "Authorization: Bearer <token>"
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    # Handler kustom agar bentuk error konsisten: { "error": "<pesan>" }
    "EXCEPTION_HANDLER": "notes.exceptions.custom_exception_handler",
}

SIMPLE_JWT = {
    # Access token tunggal berlaku 24 jam — refresh token tidak dipakai di kelas ini.
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=24),
    "AUTH_HEADER_TYPES": ("Bearer",),
    # Klaim id user diberi nama "sub" agar payload token sama dengan backend Express.
    "USER_ID_CLAIM": "sub",
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LANGUAGE_CODE = "id"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
