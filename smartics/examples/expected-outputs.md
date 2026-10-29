# Hasil Uji Contoh

Hasil `python scripts/scan_html.py examples/<nama>-dashboard` dan penilaian rubrik. Semua kredensial di contoh ini PALSU. Perintah ini dijalankan dan hasilnya sesuai harapan.

## green-dashboard: HIJAU

Scanner: 4 file, library Chart.js (lokal di `lib/`), endpoint `/api/user/login` dan `/api/v1/data/get`.

| Fitur | Status | Catatan |
|---|---|---|
| Tampilan KPI level/suhu (bobot 2) | LANGSUNG | data dari `/api/v1/data/get`, polling 2 detik |
| Login | LANGSUNG | memakai `/api/user/login` (login SmartICS) |
| Grafik trend (Chart.js lokal) | LANGSUNG | library sudah lokal |

Tidak ada SERVICE/TIDAK BISA/KONFIRMASI. Langsung 100%. Skenario B (baca tag), level 4. Rekomendasi mulai read-only.

## yellow-dashboard: KUNING

Scanner: 2 file, Chart.js dan SheetJS dari CDN, WebSocket, Telegram, `setTimeout` penjadwalan malam.

| Fitur | Status | Catatan |
|---|---|---|
| Tampilan KPI + chart (bobot 2) | LANGSUNG | penyesuaian CDN->lokal |
| Ambil data `/api/v1/data/get` | LANGSUNG | |
| Update via WebSocket | KONFIRMASI | tidak ada di Public API terdokumentasi; sarankan polling 1-5 detik |
| Kirim Telegram | ADD-ON | add-on Notifications (token bot jangan di JS public) |
| Export Excel terjadwal tiap malam | SERVICE | harus jalan tanpa browser; template bawaan = ADD-ON Reporting |

Tidak ada TIDAK BISA. Ada ADD-ON, SERVICE, KONFIRMASI, jadi KUNING. Skenario B, level 4.

## red-dashboard: MERAH

Scanner: 1 file; temuan `<?php`, `mysql.createConnection` dengan connection string, `rtsp://admin:****@192.168.x.x`, `API_KEY = "****"`. Nilai asli tidak pernah tercetak.

| Fitur | Status | Catatan |
|---|---|---|
| Kode PHP server-side | TIDAK BISA | tidak jalan di ioServer; pindah ke SERVICE |
| Koneksi database langsung dari JS | TIDAK BISA | ganti ke `/api/v1/database/query` dengan Alias |
| Stream RTSP langsung di `<video>` | SERVICE | butuh konversi stream; kredensial kamera ke `private\` |
| API key di JS | SERVICE | pindah ke `private\`; temuan keamanan |

Ada TIDAK BISA di fitur inti, jadi MERAH.
