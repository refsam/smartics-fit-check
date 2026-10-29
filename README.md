# smartics-fit-check (/smartics)

`/smartics` adalah skill Claude untuk tim sales: kamu kasih dashboard demo (file HTML, folder, zip, atau kode yang ditempel), lalu Claude bilang berapa persen yang bisa jalan di SmartICS (SSH Custom HTML Hosting), apa yang tidak bisa, dan apa yang perlu dikonfirmasi tim teknis. Hasilnya estimasi awal, bukan janji.

## Cara install

**Claude Code (pribadi)**
Salin folder `smartics/` ke `~/.claude/skills/smartics/`.
Windows: `%USERPROFILE%\.claude\skills\smartics\`

**Claude Code (per proyek)**
Salin folder `smartics/` ke `.claude/skills/smartics/` di folder proyek.

**Claude chat (claude.ai)**
Zip folder `smartics/` (pastikan `SKILL.md` ada di dalam folder itu), upload lewat pengaturan Skills.

## Cara pakai

Ketik `/smartics` lalu sebutkan dashboard-nya. Contoh:

- `/smartics cek dashboard di ./demo-pabrik/`
- `/smartics ini dashboard demo untuk customer, bisa di SmartICS?` (lampirkan file)

Di Claude chat tanpa `/`: tulis "pakai skill smartics" sambil melampirkan file HTML atau menempel kodenya.

Claude mungkin bertanya maksimal 3 hal (data dari mana, perlu tulis ke SCADA, harus jalan 24/7).

## Contoh hasil (ringkas)

```
| Penilaian                     | Hasil                                        |
| Kemudahan dikembangkan        | SEDANG                                       |
| Butuh service tambahan?       | Ya (export Excel terjadwal, Node.js/Python)  |
| Butuh add-on?                 | Ya (Notifications)                           |
| Menyentuh SCADA?              | Baca saja                                    |
| Langsung / +add-on / +service | 40% / 60% / 80%                              |

| Fitur                   | Status     | Perlu service? | Penyesuaian |
| Tampilan KPI + chart    | LANGSUNG   | Tidak          | CDN->lokal  |
| Kirim Telegram          | ADD-ON     | Tidak          | -           |
| Export Excel tiap malam | SERVICE    | Ya             | -           |
| Update via WebSocket    | KONFIRMASI | -              | polling     |
```

Contoh lengkap ada di `smartics/examples/expected-outputs.md`.

## Batasan

- Hasil adalah estimasi awal. Tidak menjanjikan harga atau waktu.
- Knowledge base mengikuti materi training SmartICS terakhir (lihat versi di `smartics/references/smartics-capabilities.md`). Hal yang tidak ada di sana akan ditandai KONFIRMASI.
- Kalau hanya screenshot, keyakinan rendah karena kode tidak terlihat.
- Skill hanya membaca file; tidak mengubah file customer dan tidak mengirim data keluar.

## Cara memperbarui knowledge base (untuk tim teknis)

1. Edit `smartics/references/smartics-capabilities.md`.
2. Naikkan nomor **Versi** di bagian atas file itu.
3. Kalau ada aturan klasifikasi baru, sesuaikan `scoring-rubric.md`.
4. Jalankan ulang scanner pada folder `smartics/examples/` dan cocokkan dengan `expected-outputs.md`.
5. Bagikan ulang folder `smartics/` ke tim sales.
