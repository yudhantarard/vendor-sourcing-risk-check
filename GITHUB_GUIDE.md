# Panduan Upload ke GitHub dan Deploy (bisa dibuka dari HP)

Hasil akhirnya: kode ada di GitHub, aplikasi jalan di Streamlit Community Cloud, dan kamu membukanya lewat satu link dari HP atau laptop. Semuanya gratis. Pencarian vendor memakai OpenStreetMap, tanpa akun dan tanpa kartu.
Tampilan menu di GitHub, Streamlit, dan Google bisa berubah. Kalau ada tombol yang beda nama, cari yang artinya sama.

## Sebelum mulai
- Akun GitHub (github.com).
- Akun Streamlit Community Cloud (share.streamlit.io). Masuk dengan akun GitHub tadi.
- Google API key itu **opsional** (Langkah 6). Tanpa key, app memakai OpenStreetMap yang gratis.
- Unzip `vendor-risk-check.zip` di laptop.

## Langkah 1. Buat repository di GitHub
1. Di github.com klik **+** di kanan atas, lalu **New repository**.
2. Nama: `vendor-sourcing-risk-check`. Pilih **Public** (kalau mau dipamerkan) atau **Private**.
3. Jangan centang pilihan tambahan apa pun. Klik **Create repository**.

## Langkah 2. Upload file lewat browser
1. Di halaman repo kosong klik **uploading an existing file**.
2. Dari folder hasil unzip, seret **isi** folder `vendor-risk-check` (bukan folder luarnya): `app.py`, `requirements.txt`, `README.md`, `GITHUB_GUIDE.md`, `.gitignore`, folder `services`, `data`, `utils`, `assets`, dan folder `.streamlit`.
3. File atau folder yang namanya diawali titik (`.gitignore`, `.streamlit`) sering tersembunyi di laptop. Kalau tidak kelihatan: di Mac tekan Cmd+Shift+titik, di Windows aktifkan **Hidden items** di tab View. Kalau tetap sulit, buat lewat **Add file > Create new file**: ketik `.streamlit/config.toml` sebagai nama (garis miring otomatis membuat folder), lalu tempel isi file aslinya.
4. Tulis pesan commit, misalnya `first upload`, lalu klik **Commit changes**.
5. Periksa daftar file di repo. **Pastikan tidak ada** `secrets.toml` (yang boleh ada hanya `secrets.toml.example`). Kalau key sempat ter-upload, anggap bocor: hapus key itu di Google Cloud dan buat yang baru.

## Langkah 3. Deploy di Streamlit Community Cloud
1. Buka share.streamlit.io, klik **Create app**, pilih deploy dari GitHub.
2. Pilih repository `vendor-sourcing-risk-check`, branch `main`, dan main file path `app.py`.
3. Klik **Advanced settings**, lalu di kotak **Secrets** tempel:
   ```
   APP_PASSWORD = "password-pilihanmu"
   ```
4. Klik **Deploy**. Tunggu beberapa menit sampai app tampil. Kalau repo-nya Private, Streamlit akan meminta izin akses ke repo itu.
5. Salin link aplikasinya dan buka dari HP. Di browser HP kamu bisa pilih **Add to Home Screen** supaya jadi ikon.

## Langkah 4. Mengubah aplikasi nanti
1. Buka file di GitHub, klik ikon pensil, edit, lalu **Commit changes**.
2. Streamlit otomatis memperbarui aplikasi dalam beberapa saat. Mau ganti daftar sektor atau kata kunci risiko: edit `data/sectors.py` atau `data/risk_keywords.py`.
3. Mengubah password: di Streamlit buka menu app, **Settings > Secrets**.

## Langkah 5 (opsional, berbayar). Pakai Google Places untuk data lebih lengkap
1. Buka console.cloud.google.com, buat project baru, lalu aktifkan penagihan (billing). Google meminta kartu, dan ada kuota gratis bulanan yang aturannya bisa berubah, jadi cek halaman harga Places API.
2. Menu **APIs & Services > Library**, cari **Places API (New)**, klik **Enable**.
3. Menu **APIs & Services > Credentials > Create credentials > API key**. Salin key-nya.
4. Klik key tersebut, di **API restrictions** pilih **Restrict key** lalu centang hanya Places API (New). Simpan.
5. Di **Billing > Budgets & alerts**, buat budget kecil dengan peringatan email supaya biaya tidak kaget.

6. Tambahkan baris `GOOGLE_PLACES_API_KEY = "key-kamu"` di Secrets Streamlit. App otomatis memakai Google, dan kembali ke OpenStreetMap kalau Google gagal.

## Keamanan dan biaya
- Jangan menulis password atau API key di file kode atau di README. Hanya di Secrets.
- `APP_PASSWORD` membuat orang yang menemukan linknya tidak bisa memakai aplikasimu (dan kuota Google kalau key dipasang). Pakai password yang tidak dipakai di tempat lain.
- App gratis bisa tertidur kalau lama tidak dipakai. Buka linknya dan klik tombol untuk membangunkan.
- OpenStreetMap gratis tapi ada batas wajar (sekitar satu permintaan per detik). Pakai untuk keperluan pribadi, jangan untuk pencarian massal.
- Google Places hanya berbayar kalau kamu memasang key. Pantau di Google Cloud Billing.

## Kalau ada masalah
- **ModuleNotFoundError**: pastikan `requirements.txt` ada di folder paling atas repo, bukan di dalam subfolder.
- **Data bertanda MOCK**: OpenStreetMap sedang tidak bisa dihubungi. Coba lagi beberapa saat.
- **Hasil sedikit atau kosong**: banyak PT B2B belum ada di OpenStreetMap. Pakai "Add a vendor manually".
- **Pesan "rejected the API key"** (hanya kalau pakai Google): Places API (New) belum di-enable, penagihan belum aktif, atau pembatasan key salah.
- **Berita tidak muncul**: Google News kadang membatasi akses. Coba lagi beberapa saat.
- **Perubahan tidak muncul**: pastikan sudah di-commit ke branch `main`, lalu pilih **Reboot** di menu app.
