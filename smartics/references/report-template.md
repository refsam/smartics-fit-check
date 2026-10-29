# Format Laporan /smartics

## Aturan output

- **Output skill = file `.txt`**, bukan jawaban biasa di chat. File ini yang nanti dicek tim teknis. Nama file: `laporan-smartics-<nama-dashboard>.txt`, disimpan di folder kerja saat ini (bukan di folder dashboard customer; jangan mengubah file customer).
- Balasan di chat setelah menyimpan: maksimal 2-3 baris berisi path lengkap file, kemudahan (MUDAH/SEDANG/SULIT), dan "detail ada di file". **Jangan menempel isi laporan ke chat.** Pertanyaan konteks (langkah 4 di SKILL.md) tetap boleh ditanyakan di chat sebelum laporan dibuat.
- Kalau tidak bisa menulis file (mis. Claude chat tanpa code execution), buat file `.txt` yang bisa diunduh jika tersedia; hanya kalau benar-benar tidak mungkin, tulis seluruh laporan dalam satu blok teks polos agar mudah disalin ke file .txt.
- Format **teks polos**, tanpa markdown: tabel dibuat dengan garis `+---+` dan `|`, lebar maksimal 100 karakter per baris supaya tidak terpotong. Judul bagian pakai huruf besar dan garis `====`.
- Bahasa Indonesia santai untuk sales. Istilah teknis diterangkan satu kalimat. Hindari emoji.
- Tabel lebar dipecah: tabel status (kolom pendek) dan daftar "penjelasan per fitur" di bawahnya, jangan satu tabel dengan kolom penuh kalimat.

## Urutan isi

### 1. KESIMPULAN CEPAT

Tabel dua kolom `Penilaian | Hasil`, dengan baris:

- Tingkat kemudahan: MUDAH / SEDANG / SULIT + 1 kalimat arti.
- Butuh service tambahan: Tidak / Ya (sebut). Keterangan: service = program kecil yang jalan terus di server.
- Butuh add-on berlisensi: Tidak / Ya (sebut nama).
- Menyentuh SCADA: Tidak / Baca saja / Baca + tulis.
- Cukup dashboard standar: CUKUP DASHBOARD STANDAR / CAMPURAN / PERLU CUSTOM HTML.
- Skenario dan level: A/B/C, Level 0-5, dengan arti singkat.

**Bagian "seberapa banyak yang bisa" ditulis begini (jangan disingkat jadi satu baris bergaris miring):**

| Penilaian | Hasil |
|---|---|
| Jumlah fitur yang dinilai | n fitur |
| Langsung bisa di SmartICS | xx% (a dari n fitur) |
| Tambahan kalau pasang add-on | +xx% (b fitur) |
| Tambahan kalau dibuatkan service | +xx% (c fitur) |
| Total bisa dengan semua tambahan | xx% |
| Belum pasti (dicek tim teknis) | xx% (e fitur), bisa naik jadi xx% bila semua ternyata bisa |
| Tidak bisa | xx% (d fitur) |

Rumus ada di scoring-rubric 5.3. "Tambahan" = selisih persen kumulatif. Pemetaan kemudahan: HIJAU = MUDAH, KUNING = SEDANG, MERAH = SULIT.

Tutup bagian ini dengan: "Struktur file (public/private, library lokal) dirapikan tim teknis, tidak mempengaruhi penilaian ini." dan "Estimasi awal, bukan janji. Perlu konfirmasi tim teknis."

### 2. ARTI STATUS

Tabel `Status | Artinya`: LANGSUNG, ADD-ON, SERVICE, TIDAK BISA, KONFIRMASI (bahasa sales, satu kalimat).

### 3. DAFTAR SEMUA FITUR

Tabel `No | Fitur | Status | Service? | Add-on? | Dashboard standar?`. Satu baris per fungsi di dashboard (bukan per baris kode), fitur inti dulu. Dashboard standar = BISA / ADD-ON / SEBAGIAN / TIDAK / KONFIRMASI (scoring-rubric 5.6).

Di bawahnya, "PENJELASAN PER FITUR": untuk tiap nomor, 2-3 baris:
- Apa ini (bahasa awam)
- Widget/fitur standar yang setara (dari widget-catalog.md) dan bedanya dengan demo
- Penyesuaian (mis. data contoh -> tag) dan lokasi di kode (file:baris)

### 4. PERLU SERVICE ATAU TIDAK

Dua daftar/tabel pendek:
- Fitur TANPA service (nomor + nama).
- Fitur PERLU service: nomor, kenapa tidak cukup di halaman, teknologi umum (Node.js/Python, Windows Service/Task Scheduler), ditaruh di `private\namaapp\service\`.
Kalau tidak ada: "Tidak ada fitur yang perlu service."

### 5. YANG TIDAK BISA DAN YANG PERLU DICEK

Tabel `Fitur | Masalahnya | Alternatif / pertanyaan ke tim teknis`. Pertanyaan kalimat lengkap dan spesifik.

### 6. TEMUAN KEAMANAN

Tabel `Lokasi | Jenis | Nilai (disamarkan) | Saran`. Jangan pernah menulis nilai asli. "Tidak ada temuan" bila kosong.

### 7. CARA BICARA KE CUSTOMER

Dua daftar: BOLEH BILANG dan JANGAN BILANG, disesuaikan hasil. Jangan menyebut harga atau waktu.

### 8. LANGKAH BERIKUTNYA

1. Isi Custom Request Form.
2. Jawab 5 Kenapa yang disesuaikan dengan dashboard ini (lima pertanyaan konkret, bukan generik).
3. Kirim ke tim teknis bersama laporan ini dan file dashboard.
