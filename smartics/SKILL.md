---
name: smartics
description: Cek apakah demo dashboard custom HTML (file, folder, zip, kode yang ditempel, atau screenshot) bisa didukung SmartICS (SSH Custom HTML Hosting). Gunakan saat sales menjalankan /smartics, atau bertanya "dashboard ini bisa di SmartICS?", "berapa persen didukung?", "butuh Node.js/middleware?". Menghasilkan laporan kesiapan, persentase, daftar yang tidak bisa, dan kebutuhan service tambahan.
---

# /smartics - SmartICS Fit Check

Tugasmu: menilai apakah dashboard custom HTML bisa jalan di SmartICS (SSH Custom HTML Hosting). Hasilnya **estimasi awal, bukan janji**. Pakai bahasa Indonesia santai.

## Langkah

1. **Terima input.** Bisa path file/folder/zip, kode HTML yang ditempel, atau screenshot/PDF. Kalau kosong, minta sales melampirkan file atau menempel kodenya. Kalau hanya screenshot, tetap analisis tapi tulis jelas "tingkat keyakinan rendah, karena kode tidak terlihat" dan minta file aslinya.
2. **Baca referensi** (satu kali, di awal):
   - `references/smartics-capabilities.md` (satu-satunya sumber fakta)
   - `references/scoring-rubric.md`
   - `references/service-patterns.md`
   - `references/widget-catalog.md` (widget dashboard standar)
   - `references/report-template.md`
3. **Jalankan scanner** kalau bisa menjalankan kode: `python scripts/scan_html.py <path>` (path relatif terhadap folder skill ini). Kalau tidak bisa (misal Claude chat tanpa code execution), periksa manual dengan daftar cek di `scoring-rubric.md` bagian 5.2.
4. **Tanya konteks seperlunya** (maksimal 3 pertanyaan sekaligus): data aslinya dari mana (tag SCADA, database, input manual), perlu menulis balik ke SCADA atau tidak, harus jalan 24/7 tanpa browser atau tidak. Kalau jawabannya sudah jelas dari kode, jangan tanya.
5. **Klasifikasikan** tiap fitur dengan rubrik, hitung persen, tentukan skenario (A/B/C) dan level (0-5). Scanner hanya mendeteksi; keputusan status ada di kamu.
6. **Tulis laporan ke file .txt.** Sesuai `references/report-template.md`, simpan sebagai `laporan-smartics-<nama>.txt` di folder kerja (bukan di folder dashboard customer). **Hasil akhirnya adalah file itu, bukan jawaban panjang di chat**, karena file akan dicek tim teknis. Di chat cukup 2-3 baris: path file, lampu/kemudahan, dan satu kalimat "detail ada di file". Jangan menempel isi laporan ke chat.

## Aturan kejujuran

- Hanya bilang "didukung" untuk hal yang tertulis di knowledge base. Selain itu: **KONFIRMASI**.
- Jangan menjanjikan harga, waktu, atau hasil.
- Jangan menyimpulkan lebih dari yang terlihat di kode.

## Fokus: fitur, bukan struktur folder

Demo biasanya belum rapi menurut standar SmartICS (public/private, CDN, dll). Itu dibereskan tim teknis nanti dan tidak mempengaruhi penilaian. Cukup tulis satu baris di laporan: "Struktur file dirapikan tim teknis". Nilai hanya fitur-fiturnya (lihat `scoring-rubric.md`, bagian "struktur file TIDAK dinilai").

## Aturan keamanan

Kalau menemukan password, API key, token, atau URL RTSP berkredensial di kode: **jangan tulis ulang nilainya**. Sebut lokasinya (file:baris), tampilkan nilai yang disamarkan (contoh `rtsp://admin:****@192.168.x.x`), dan sarankan memindahkannya ke folder `private\`.

## Contoh pemakaian

- `/smartics cek dashboard di ./demo-pabrik/`
- `/smartics ini dashboard demo untuk customer, bisa di SmartICS?` (lampirkan file HTML)
- "Pakai skill smartics: berapa persen dashboard ini yang langsung jalan, dan butuh Node.js nggak?" (tempel kode)

## Yang TIDAK dilakukan skill ini

- Tidak mengubah file customer (hanya membaca).
- Tidak mengirim data keluar (scanner tanpa panggilan jaringan).
- Tidak memberi harga atau estimasi waktu pengerjaan.
