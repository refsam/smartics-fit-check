# Rubrik Penilaian

## 5.1 Lima status per fitur

| Status | Arti |
|---|---|
| LANGSUNG | Jalan di custom HTML + Public API/database query tanpa tambahan (boleh dengan penyesuaian kecil seperti mengganti data dummy ke tag) |
| ADD-ON | Butuh modul add-on berlisensi (knowledge base bagian 7) |
| SERVICE | Butuh service tambahan di `private\` (Node.js/Python/middleware/Task Scheduler) |
| TIDAK BISA | Tidak mungkin di SmartICS seperti adanya (mis. browser langsung ke PLC/driver, koneksi DB langsung dari front-end, kode server-side jalan di ioServer) |
| KONFIRMASI | Tidak tercantum di knowledge base, tanya tim teknis |

Selain status, beri tanda **penyesuaian** bila HTML perlu diubah: `CDN->lokal`, `dummy->tag`, `hardcode->DB query`, `secret->private`, `login sendiri->login SmartICS`.

### Aturan: struktur file TIDAK dinilai

Demo dari sales biasanya belum mengikuti standar SmartICS (pemisahan `public\` dan `private\`, 1 app = 1 subfolder, library lokal). Itu **dirapikan tim teknis nanti** dan **tidak boleh menurunkan lampu atau persen**. Yang dinilai hanya fitur: apa yang dilakukan dashboard dan apakah bisa di SmartICS.

Yang termasuk "rapikan teknis" (cukup satu baris catatan di laporan, bukan status per fitur):
- Penempatan file ke `public\namaapp\` dan `private\namaapp\`.
- CDN -> lokal (tetap dicatat di kolom Penyesuaian, tapi fitur tetap LANGSUNG).
- Secret yang tercecer di JS dipindah ke `private\` (tetap dilaporkan sebagai temuan keamanan, tapi tidak mengubah status fitur yang bukan soal service).
- Pembersihan file tak terpakai, penamaan, versi/backup.

Yang tetap dinilai (bukan sekadar struktur): kode server-side, koneksi DB langsung dari front-end, RTSP, WebSocket, proses 24/7, dan sejenisnya, karena itu menyangkut fitur.

## 5.2 Daftar cek (dipakai scanner dan pemeriksaan manual)

Nomor di bawah = nomor `check` di output scanner.

1. **Resource eksternal** (CDN script/CSS/font/gambar): LANGSUNG dengan penyesuaian CDN->lokal.
2. **Panggilan `/api/v1/...` atau `/api/user/...`**: LANGSUNG (SmartICS API). Catat tag atau endpoint yang dipakai.
3. **fetch/axios/XMLHttpRequest ke URL absolut luar** (bukan SmartICS): SERVICE (proxy/middleware) bila server luarnya wajib dipakai; KONFIRMASI bila tidak jelas.
4. **WebSocket / EventSource / MQTT.js di browser**: KONFIRMASI (tidak ada di Public API yang terdokumentasi), sarankan polling 1-5 detik.
5. **Data dummy/mock** (Math.random, array hardcode, JSON statis): LANGSUNG dengan penyesuaian dummy->tag atau hardcode->DB query.
6. **Form login buatan sendiri, tabel user sendiri**: LANGSUNG dengan penyesuaian login sendiri->login SmartICS.
7. **Secret di kode** (password, API key, token, URL RTSP berkredensial): flag keamanan, SERVICE (pindah ke `private`).
8. **`<video>` / RTSP / HLS**: RTSP butuh SERVICE (konversi stream).
9. **getUserMedia, mikrofon, push to talk**: SERVICE.
10. **Peta** (Leaflet/Google Maps/dll): LANGSUNG sebagai halaman custom (contoh GPS Tracker), catatan tile peta butuh internet; atau ADD-ON Maps/GIS bila customer ingin modul bawaan.
11. **Chart/3D** (Chart.js, ECharts, three.js): LANGSUNG bila library disimpan lokal.
12. **Export PDF/Excel dari browser** (jsPDF, SheetJS, print): LANGSUNG. Export terjadwal/otomatis tanpa browser: SERVICE. Template laporan bawaan: ADD-ON Reporting.
13. **Kirim e-mail/Telegram**: ADD-ON Notifications. WhatsApp atau SMTP custom: SERVICE.
14. **Sinkron ke cloud/ERP/database lain**: SERVICE (atau ADD-ON Database Exchange bila hanya baca/tulis database).
15. **Koneksi database langsung dari front-end** (connection string, SQL di JS): TIDAK BISA seperti adanya; ubah ke `/api/v1/database/query` dengan Alias, atau lewat SERVICE.
16. **Kode server-side di proyek** (PHP, ASP.NET, Flask, Express, Next.js SSR): TIDAK BISA jalan di ioServer, pindahkan ke SERVICE. Hasil build statis (dist/build) boleh di public.
17. **Framework dengan build step** (React/Vue/Vite): LANGSUNG bila hanya hasil build statis yang di-host.
18. **Proses latar** (setInterval untuk simpan/log/hitung yang harus jalan terus): SERVICE bila harus berjalan tanpa browser.
19. **Upload file ke server atau tulis file ke folder**: SERVICE.
20. **Koneksi langsung ke PLC/driver dari browser**: TIDAK BISA.
21. **Menulis ke tag (`/api/v1/item/set`)**: LANGSUNG secara teknis, tapi menyentuh SCADA, butuh persetujuan terpisah.
22. **Redundancy**: KONFIRMASI.

## 5.3 Rumus persen

Hitung per fitur (satu fungsi yang terlihat di dashboard, bukan per baris kode). Bobot default 1; fitur inti (tampilan utama dashboard, atau yang disebut sales sebagai wajib) bobot 2.

- Langsung % = LANGSUNG / total
- Dengan add-on % = (LANGSUNG + ADD-ON) / total
- Dengan service tambahan % = (LANGSUNG + ADD-ON + SERVICE) / total
- Tidak bisa % = TIDAK BISA / total
- Perlu konfirmasi % = KONFIRMASI / total

(Semua dihitung dengan bobot.) Tampilkan sebagai angka bulat dengan kata-kata jelas (lihat report-template bagian 1: "Langsung bisa", "Tambahan kalau pasang add-on", "Tambahan kalau dibuatkan service", "Total"), bukan satu baris bergaris miring. Beri rentang bila ada KONFIRMASI: batas bawah = semua KONFIRMASI dianggap tidak bisa; batas atas = semua dianggap bisa.

Selalu tulis: "Estimasi awal, bukan janji. Perlu konfirmasi tim teknis."

## 5.4 Lampu penilaian

- **HIJAU:** tidak ada TIDAK BISA dan tidak ada SERVICE, KONFIRMASI paling banyak 1.
- **KUNING:** tidak ada TIDAK BISA di fitur inti, tapi ada SERVICE, ADD-ON, atau KONFIRMASI.
- **MERAH:** ada TIDAK BISA di fitur inti, atau lebih dari separuh fitur berstatus KONFIRMASI.

## 5.5 Skenario dan level

- Dashboard memakai tag/DB SCADA (data/get, item/set) = **Skenario B** (menyentuh SCADA, perlu uji ekstra, mulai read-only).
- Tidak menyentuh SCADA = **Skenario C**.
- Tujuan jadi produk reusable banyak customer (seperti CMMS) = **Skenario A**.

Level: 0 fitur standar, 1 konfigurasi, 2 add-on, 3 custom HTML tanpa SCADA, 4 custom HTML yang menyentuh SCADA, 5 full custom / produk baru. Tentukan level tertinggi yang diperlukan dashboard.

## 5.6 Bisa dengan dashboard standar? (kolom tambahan)

Untuk setiap fitur, nilai juga: **apakah bisa dibuat dengan dashboard standar SmartICS + widget + fitur standar/add-on, tanpa custom HTML?** Pakai `widget-catalog.md`.

| Nilai | Arti |
|---|---|
| BISA | Ada widget/fitur standar yang setara |
| ADD-ON | Bisa dengan dashboard standar + add-on berlisensi |
| SEBAGIAN | Ada widget yang mendekati, tapi tampilan/perilaku persis bisa berbeda; sebut bagian yang beda |
| TIDAK | Tidak ada padanan standar: perlu custom HTML (atau service) |
| KONFIRMASI | Nama widget ada tapi perilakunya belum terverifikasi, atau tidak tercantum |

Kesimpulan keseluruhan (satu baris di laporan): **CUKUP DASHBOARD STANDAR** (semua BISA/ADD-ON), **CAMPURAN** (sebagian standar, sebagian custom HTML), atau **PERLU CUSTOM HTML** (fitur inti TIDAK/SEBAGIAN). Nilai ini terpisah dari lampu 5.4: lampu menjawab "bisa di SmartICS?", kolom ini menjawab "perlu custom HTML atau tidak?".
