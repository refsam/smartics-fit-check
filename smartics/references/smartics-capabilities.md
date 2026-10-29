# SmartICS Capabilities (Knowledge Base)

**Versi:** 1.1
**Sumber:** materi training SSH SmartICS Custom HTML Hosting + daftar fitur standar/add-on SmartICS + slide SmartICS_Technical New (protokol, database, add-on) + folder widgets (katalog di `widget-catalog.md`).

> Jika tidak ada di file ini, statusnya **KONFIRMASI**.

## 1. Apa itu SSH SmartICS

- Fitur SmartICS ioServer yang meng-host halaman web sendiri (HTML, CSS, JavaScript) langsung di server.
- Tidak perlu web server tambahan (tanpa IIS, Nginx, Apache).
- Same origin dengan SmartICS: login, roles, tag, dan database langsung bisa dipakai. Halaman memanggil API langsung, tanpa CORS dan tanpa middle server.
- Folder hosting: Windows `C:\ProgramData\SmartICS\ioServer\hosting\`, Linux `/etc/SmartICS/ioServer/hosting/`.
- `public\`: dibuka oleh browser (HTML, CSS, JS, gambar, library frontend). Semua orang bisa melihat file ini (View Source).
- `private\`: tidak pernah dibuka browser (backend Node.js/Python, secret seperti `.env` dan sertifikat, SQL script, backup, manual, hasil dan log).
- URL: `https://<server>:5001/public/<path file>`. Contoh: `hosting\public\namaapp\index.html` menjadi `https://localhost:5001/public/namaapp/index.html`.
- Rekomendasi struktur: 1 app = 1 subfolder, nama sama di `public\namaapp\` dan `private\namaapp\`.
- Setelah update file, tekan Ctrl+F5 untuk menghindari cache lama.

## 2. Yang bisa dilakukan halaman custom (public)

- Read dan write tag, realtime.
- Read dan write database.
- Memakai SmartICS users dan roles.
- Contoh yang sudah pernah dibuat: custom web report (tabel, filter, export, PDF print), form operator (input data, checklist, approval), mini MES app, dashboard desain bebas, layar TV/produksi, advance custom widget, widget builder, 3D view, GPS tracker (peta), RTSP CCTV, AI camera, push to talk, auto-save file ke folder, MFA (Entra, DB, e-mail).

## 3. Public API (satu-satunya jalur data)

| Fungsi | Endpoint |
|---|---|
| Login (sesi disimpan di cookie) | `POST /api/user/login` |
| User dan role (401 = belum login) | `GET /api/v1/User` |
| Daftar device dan item | `/api/v1/devices/config/get` |
| Baca nilai tag | `/api/v1/data/get` |
| Tulis nilai tag | `/api/v1/item/set` |
| Query database (kirim Alias, bukan connection string) | `/api/v1/database/query` |

Dua jalur data:

- **Realtime:** Public API, polling tiap 1 sampai 5 detik.
- **Historis:** database SmartICS, lewat `/api/v1/database/query` (pakai Alias) atau koneksi langsung dari service ke PostgreSQL/MSSQL. Cocok untuk laporan, trend, total shift dan harian.

Aturan keras: tidak ada jalur lain. Halaman custom tidak bisa terhubung langsung ke driver SmartICS (Modbus, OPC UA, MQTT, S7).

Tidak ada WebSocket/push dalam materi yang tersedia: perlakukan realtime sebagai polling dan tandai kebutuhan "push realtime" sebagai KONFIRMASI.

## 4. Kapan butuh service tambahan (folder private)

Halaman hanya hidup selama browser terbuka. Butuh service tambahan untuk:

- Proses 24 jam: timer, logika, auto-save.
- Membuat PDF/Excel otomatis, menyimpan ke folder (lokal atau network).
- E-mail dan chat: SMTP, WhatsApp, Telegram.
- Sinkronisasi ke sistem lain: cloud, ERP, database lain.
- Menyimpan secret dengan aman: password DB dan SMTP.
- Backend/proxy untuk halaman yang ada di server lain.
- Mengubah stream RTSP CCTV agar bisa diputar di web (browser tidak bisa memutar RTSP langsung).
- Analisis video AI, push to talk (suara diteruskan ke user lain).

Pola: kode di `private\`, memakai Public API yang sama, dijalankan sebagai Windows Service atau Task Scheduler (Node.js/Python).

## 5. Best practice SmartICS

- Secret hanya di `private`, tidak pernah di JavaScript public.
- Pakai login SmartICS, jangan membuat sistem user sendiri.
- Library disimpan lokal, tanpa CDN, supaya jalan tanpa internet.
- Backup sebelum update, beri versi pada nama file atau zip.

## 6. Fitur standar SmartICS (tanpa biaya tambahan)

Widget Library, Event Logs (Alarm, User Login/Out, ET), Trend Lines, Users & Roles, iFrame, Backup & Restore, Pop-ups, Structured Tags, Mobile Layout, Widget Rotation.

## 7. Add-on SmartICS (opsional, berlisensi)

- Reporting (template laporan siap cetak)
- Scripting (logika custom)
- REST API (aplikasi lain menarik data SmartICS)
- Maps/GIS
- Notifications (Telegram dan e-mail)
- Database Exchange (baca dan tulis database: create, read, update, delete)

## 8. Spesifikasi teknis (dari slide Technical New)

- Sistem operasi: Windows 10 Pro/Enterprise 64-bit, Windows Server 2012 64-bit atau lebih baru, Linux 64-bit (Alpine, Ubuntu, Arch, Alt Linux, Fedora, dll), atau Docker.
- Minimum: Intel Core i3-6100, RAM 4 GB, disk kosong 11 GB.
- 8 protokol: Modbus RTU, Modbus TCP, MQTT, IEC 60870-5-104, SNMP, OPC UA Client, BACnet, S7 Client (slide lain menyebut juga CNC Focas).
- Database: PostgreSQL, MS SQL, MySQL.
- Penyebaran: on-premise atau cloud. Server SmartICS cukup PC/laptop berisi SmartICS; akses dashboard dari PC, tablet, atau HP.
- Catatan: protokol dipakai oleh **ioServer** untuk membaca device. Halaman custom tetap hanya lewat Public API (bagian 3).

## 9. Dashboard standar dan widget

Dashboard SmartICS bisa disusun dari Widget Library tanpa menulis HTML. Katalog widget dan pemetaan kebutuhan -> widget ada di `widget-catalog.md`. Perilaku detail widget yang tidak tertulis di sana = KONFIRMASI.

## 10. Detail add-on (dari slide)

- **Reporting:** template laporan (.mrt, Stimulsoft), isi otomatis dari data live, ekspor PDF. Cocok untuk shift log harian dan ringkasan bulanan. Penjadwalan otomatis tidak disebut: KONFIRMASI.
- **Maps / GIS:** lokasi site sebagai pin di peta, warna status, klik untuk detail live.
- **Scripting:** perhitungan khusus dan logika kondisi ("jika ini dan itu, maka...").
- **REST API:** aplikasi lain (ERP, website, mobile app, Power BI) menarik data SmartICS.
- **Notifications:** pesan otomatis ke Telegram atau e-mail saat nilai melewati batas.
- **Database Exchange:** baca dan tulis database lain (create, read, update, delete).

## 11. Belum terkonfirmasi

Redundancy disebut sebagai fitur SmartICS, tetapi belum jelas termasuk standar atau add-on. Statusnya selalu **KONFIRMASI** sampai file ini diperbarui.
