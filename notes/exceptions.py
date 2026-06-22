"""Handler error kustom agar bentuk respons error konsisten dengan kontrak API:
{ "error": "<pesan>" } — sama dengan backend Express, sehingga mudah dibaca
di tab Network browser saat mendiagnosis masalah deployment.
"""
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return None

    if isinstance(exc, NotAuthenticated):
        response.data = {"error": "token tidak ditemukan"}
    elif isinstance(exc, AuthenticationFailed):
        response.data = {"error": "token tidak valid"}
    elif response.status_code == 404:
        response.data = {"error": "catatan tidak ditemukan"}
    elif isinstance(response.data, dict) and "detail" in response.data:
        response.data = {"error": str(response.data["detail"])}

    return response
