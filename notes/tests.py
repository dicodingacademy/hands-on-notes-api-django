"""Unit test validasi serializer — berjalan di SQLite (settings dev),
sehingga `python manage.py test` tidak butuh PostgreSQL (termasuk di CI).
"""
from django.contrib.auth.models import User
from django.test import TestCase

from .serializers import NoteSerializer, RegisterSerializer


class RegisterSerializerTest(TestCase):
    def test_data_valid_lolos_validasi(self):
        serializer = RegisterSerializer(
            data={"username": "budi", "password": "rahasia123"}
        )
        self.assertTrue(serializer.is_valid())

    def test_username_terlalu_pendek_ditolak(self):
        serializer = RegisterSerializer(data={"username": "ab", "password": "rahasia123"})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors["username"][0]), "username harus 3-50 karakter"
        )

    def test_username_lebih_dari_50_karakter_ditolak(self):
        serializer = RegisterSerializer(
            data={"username": "a" * 51, "password": "rahasia123"}
        )
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors["username"][0]), "username harus 3-50 karakter"
        )

    def test_username_kosong_ditolak(self):
        serializer = RegisterSerializer(data={"password": "rahasia123"})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(str(serializer.errors["username"][0]), "username wajib diisi")

    def test_password_kurang_dari_6_karakter_ditolak(self):
        serializer = RegisterSerializer(data={"username": "budi", "password": "12345"})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors["password"][0]), "password minimal 6 karakter"
        )

    def test_username_duplikat_ditolak(self):
        User.objects.create_user(username="budi", password="rahasia123")
        serializer = RegisterSerializer(
            data={"username": "budi", "password": "rahasia123"}
        )
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors["username"][0]), "username sudah digunakan"
        )

    def test_password_di_hash_saat_disimpan(self):
        serializer = RegisterSerializer(
            data={"username": "budi", "password": "rahasia123"}
        )
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertNotEqual(user.password, "rahasia123")
        self.assertTrue(user.check_password("rahasia123"))


class NoteSerializerTest(TestCase):
    def test_data_valid_lolos_validasi(self):
        serializer = NoteSerializer(
            data={"title": "Belajar deployment", "body": "Materi EC2"}
        )
        self.assertTrue(serializer.is_valid())

    def test_title_kosong_ditolak(self):
        serializer = NoteSerializer(data={"title": "", "body": "isi"})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(str(serializer.errors["title"][0]), "title wajib diisi")

    def test_tanpa_title_ditolak(self):
        serializer = NoteSerializer(data={"body": "isi"})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(str(serializer.errors["title"][0]), "title wajib diisi")

    def test_title_lebih_dari_100_karakter_ditolak(self):
        serializer = NoteSerializer(data={"title": "a" * 101})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors["title"][0]), "title maksimal 100 karakter"
        )

    def test_body_boleh_kosong(self):
        serializer = NoteSerializer(data={"title": "Tanpa isi"})
        self.assertTrue(serializer.is_valid())
