# Pola Service Tambahan

Halaman custom hanya hidup selama browser terbuka. Kalau butuh sesuatu yang harus jalan sendiri, perlu **service** kecil di folder `private\`.

## Alur umum

```
Browser --> ioServer (Public API) --> Device / Database
                  ^
                  |  (Public API yang sama)
Service (private\) <--> ioServer (Public API) --> Outputs (PDF, e-mail, cloud, dll)
```

Semua pola di bawah sama: **kode di `private\namaapp\service\`**, **data lewat Public API yang sama** (login SmartICS), **jalan sebagai Windows Service atau Task Scheduler**, teknologi umum **Node.js atau Python**. Beda hanya pada tugasnya.

## Daftar pola

**Proses 24/7 (timer, logika, auto-save)**
Apa: program yang jalan terus tanpa menunggu browser. Kenapa: setInterval di halaman mati saat tab ditutup. Pakai: Node.js/Python sebagai Windows Service.

**Laporan otomatis PDF/Excel**
Apa: buat file laporan terjadwal (tiap shift/malam) dan simpan ke folder lokal atau network. Kenapa: export di browser butuh orang menekan tombol. Pakai: Python/Node.js + Task Scheduler, data dari `/api/v1/database/query`. (Template siap cetak bawaan = add-on Reporting.)

**E-mail, WhatsApp, Telegram**
Apa: kirim notifikasi. E-mail dan Telegram standar = add-on Notifications. WhatsApp dan SMTP custom = service. Kenapa: kredensial tidak boleh ada di JS public.

**Sinkron cloud / ERP / database lain**
Apa: service membaca data SmartICS lalu mengirim ke sistem lain (atau sebaliknya). Kalau hanya baca/tulis database, cek add-on Database Exchange dulu.

**Secret management**
Apa: password DB, SMTP, API key disimpan di `.env` di `private\`. Halaman memanggil service/Public API, bukan memegang secret.

**Proxy / backend**
Apa: perantara untuk halaman yang butuh data dari server luar. Kenapa: kunci API tidak boleh di browser, dan server luar sering menolak CORS.

**Konversi RTSP CCTV**
Apa: ubah stream RTSP menjadi format yang bisa diputar browser (mis. HLS/WebRTC). Kenapa: browser tidak bisa memutar RTSP langsung. Kredensial kamera disimpan di `private\`.

**AI camera**
Apa: service menganalisis video (deteksi objek dll) lalu menulis hasil ke tag/database lewat Public API. Butuh spesifikasi PC yang cukup: tanyakan tim teknis.

**Push to talk**
Apa: suara dari satu user diteruskan ke user lain. Kenapa: butuh relay audio di server; browser hanya menangkap mikrofon (getUserMedia).

**MFA (Entra, DB, e-mail)**
Apa: langkah verifikasi tambahan saat login. Pernah dibuat sebagai contoh; detail implementasi dikonfirmasi tim teknis.

## Catatan untuk sales

Service = kerjaan tambahan di sisi tim teknis (instalasi, jadwal, monitoring). Jangan menjanjikan harga atau waktu; teruskan ke tim teknis.
