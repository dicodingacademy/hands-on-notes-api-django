import os

import requests as http_requests
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .models import Classification, Note
from .serializers import NoteSerializer, RegisterSerializer

# URL layanan AI eksternal dibaca dari environment (AI_SERVICE_URL) —
# sama seperti konfigurasi lain, tidak pernah di-hardcode.
AI_URL = os.environ.get("AI_SERVICE_URL")



def first_error(errors):
    """Ambil satu pesan error pertama dari serializer.errors."""
    first_field_errors = next(iter(errors.values()))
    return str(first_field_errors[0])


def health(request):
    # Endpoint publik untuk memverifikasi server hidup —
    # dipakai saat cek deployment (EC2, NGINX, Docker). Jangan diproteksi auth.
    return JsonResponse({"status": "ok from django", "version": "1.0"})


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": first_error(serializer.errors)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = serializer.save()
        return Response(
            {"data": {"id": user.id, "username": user.username}},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username") or ""
        password = request.data.get("password") or ""
        if not username.strip():
            return Response({"error": "username wajib diisi"}, status=400)
        if not password:
            return Response({"error": "password wajib diisi"}, status=400)

        user = authenticate(username=username.strip(), password=password)
        if user is None:
            return Response({"error": "username atau password salah"}, status=400)

        # Access token tunggal (24 jam) berisi klaim { sub: userId } —
        # SIGNING_KEY-nya adalah SECRET_KEY yang dibaca dari environment.
        access_token = AccessToken.for_user(user)
        return Response({"data": {"accessToken": str(access_token)}})


class NoteListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notes = Note.objects.filter(user=request.user)
        serializer = NoteSerializer(notes, many=True)
        return Response({"data": serializer.data})

    def post(self, request):
        serializer = NoteSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": first_error(serializer.errors)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        note = serializer.save(user=request.user)
        return Response(
            {"data": NoteSerializer(note).data}, status=status.HTTP_201_CREATED
        )


class NoteDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_note(self, request, note_id):
        # Catatan milik user lain juga menghasilkan 404 (bukan 403)
        # agar tidak membocorkan keberadaan resource.
        return Note.objects.filter(id=note_id, user=request.user).first()

    def get(self, request, note_id):
        note = self.get_note(request, note_id)
        if note is None:
            return Response({"error": "catatan tidak ditemukan"}, status=404)
        return Response({"data": NoteSerializer(note).data})

    def delete(self, request, note_id):
        note = self.get_note(request, note_id)
        if note is None:
            return Response({"error": "catatan tidak ditemukan"}, status=404)
        note.delete()
        return Response({"data": {"id": note_id}})


class ClassifyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        uploaded = request.FILES.get("file")
        if not uploaded:
            return Response({"error": "file gambar wajib disertakan"}, status=400)

        # 1. Teruskan gambar ke layanan AI
        try:
            # Elemen ketiga (content_type) wajib: tanpa itu requests mengirim
            # application/octet-stream, dan layanan AI menolaknya (400, bukan gambar).
            ai_response = http_requests.post(
                f"{AI_URL}/predict",
                files={"file": (uploaded.name, uploaded.read(), uploaded.content_type)},
                timeout=30,
            )
            ai_response.raise_for_status()
            predictions = ai_response.json()["predictions"]
        except http_requests.Timeout:
            return Response({"error": "layanan AI terlalu lama merespons"}, status=504)
        except http_requests.RequestException:
            return Response({"error": "gagal menghubungi layanan AI"}, status=502)

        # 2. Simpan hasil ke database (kegagalan simpan tidak membatalkan respons ke FE)
        top_result = predictions[0]
        try:
            Classification.objects.create(
                user=request.user,
                image_name=uploaded.name,
                top_label=top_result["label"],
                top_confidence=top_result["confidence"],
                all_predictions=predictions,
            )
        except Exception:
            pass

        # 3. Kembalikan hasil ke Front-End
        return Response({"data": {"predictions": predictions}})
