# Notes API — Django

API catatan sederhana dengan autentikasi JWT. Dibangun dengan Django, Django REST Framework, dan SimpleJWT (access token saja, tanpa refresh token).

## Persyaratan

- Python 3.12 atau lebih baru
- PostgreSQL (hanya untuk mode produksi — pengembangan dan test memakai SQLite)

## Menjalankan Secara Lokal

1. Buat dan aktifkan virtual environment, lalu pasang dependensi:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Jalankan migrasi (mode dev memakai SQLite, tanpa konfigurasi tambahan):

   ```bash
   python manage.py migrate
   ```

3. Jalankan server pengembangan:

   ```bash
   python manage.py runserver 8000
   ```

4. Cek server hidup:

   ```bash
   curl http://localhost:8000/api/health
   # → {"status": "ok"}
   ```

## Menjalankan Test

Test memakai SQLite — **tidak butuh PostgreSQL**:

```bash
python manage.py test
```

## Mode Produksi (Gunicorn)

Mode produksi memakai `project/settings/prod.py` yang membaca semua konfigurasi dari environment (lihat tabel di bawah dan `.env.example`):

```bash
gunicorn project.wsgi
```

## Menguji dengan Postman

Impor file `postman_collection.json` ke Postman (Import → pilih file). Urutan pemakaian:

1. **Health Check** — memastikan server hidup.
2. **Auth → Register** — username unik dibuat otomatis setiap dijalankan.
3. **Auth → Login** — access token otomatis tersimpan ke variabel koleksi.
4. Folder **Catatan** — langsung bisa dipakai karena token sudah terpasang.

Untuk menguji server yang sudah di-deploy, ubah variabel koleksi `baseUrl`.

## Variabel Environment (produksi)

| Variabel | Fungsi | Contoh |
|---|---|---|
| `SECRET_KEY` | Kunci rahasia Django (juga penandatangan JWT) | (string acak yang panjang) |
| `DATABASE_URL` | Alamat koneksi PostgreSQL | `postgres://user:pass@localhost:5432/notes_db` |
| `ALLOWED_HOSTS` | Daftar host yang diizinkan, dipisah koma | `localhost,127.0.0.1` |
| `CORS_ALLOWED_ORIGINS` | Daftar origin frontend yang diizinkan, dipisah koma | `http://localhost:5173` |

## Daftar Endpoint

| Method | Endpoint | Auth | Fungsi |
|---|---|---|---|
| GET | `/api/health` | — | Cek server hidup |
| POST | `/api/auth/register` | — | Daftar user baru |
| POST | `/api/auth/login` | — | Masuk, mendapat access token |
| GET | `/api/notes` | Bearer | Daftar catatan milik user |
| POST | `/api/notes` | Bearer | Buat catatan |
| GET | `/api/notes/:id` | Bearer | Detail catatan |
| DELETE | `/api/notes/:id` | Bearer | Hapus catatan |
