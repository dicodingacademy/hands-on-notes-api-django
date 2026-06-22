"""Entry point WSGI — dijalankan Gunicorn di produksi: `gunicorn project.wsgi`."""
import os

from django.core.wsgi import get_wsgi_application

# Default ke settings prod karena WSGI hanya dipakai di server produksi.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.prod")

application = get_wsgi_application()
