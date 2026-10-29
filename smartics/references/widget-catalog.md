# Katalog Widget Dashboard Standar SmartICS

**Sumber:** isi folder `widgets\` (nama file widget) + slide "SmartICS_Technical New" (fitur standar dan add-on).
**Catatan kejujuran:** daftar ini berdasarkan **nama widget**. Perilaku detail (animasi, warna otomatis, binding ke tag) belum terverifikasi dari file; kalau sebuah tampilan butuh perilaku spesifik widget, statusnya **KONFIRMASI** sampai tim teknis cek.

Dashboard standar = layar yang disusun dari widget di atas, tanpa menulis HTML sendiri. Semua widget ini bagian dari fitur standar "Widget Library" (tanpa biaya tambahan).

| Kategori | Widget | Cocok untuk |
|---|---|---|
| Common | DateTime, IFrame, Image, LinkButton, Map, TextNote, Value, VideoStream | Angka nilai tag, teks, gambar/logo, link antar layar, embed halaman web, jam, peta (widget Map), video |
| Analog | AnalogChip, TextCondition | Nilai analog dalam chip; teks berubah menurut kondisi nilai |
| Discrete | DiscreteChip, DiscreteLamp | Status on/off, run/stop, alarm sebagai lampu atau chip |
| Gauge | AngularGauge(2), BarGauge(1-3), BulletGauge(1-3), DonutGauge, QuarterGauge | Level, suhu, tekanan, beban dalam bentuk dial/bar |
| Analytics | Bar, Bars, Pie | Grafik batang dan pie |
| Trend | LiveTrend, MultiLiveTrend | Grafik tren satu atau banyak tag |
| Tables | DatasetTable, ParametersTable, SnmpTrapOidsTable | Tabel data, tabel parameter, tabel SNMP trap |
| Command | CommandButton, CommandInput, OnOffButton, Selector, ToggleButton | Kontrol: tombol, input nilai, on/off, pilihan (menulis ke tag) |
| Indicators | Indicator1-6, IndicatorLamp, Fire, Fire2 | Indikator status dan alarm kebakaran |
| Light | Lamp, LampOutside | Lampu |
| Measurer | ElectricityMeter, FlowMeter1-2, HeatMeter, Manometer, Recloser, SignalLevel | Meter listrik/aliran/panas, tekanan, recloser, kekuatan sinyal |
| Transformer | Battery, Breaker, Circles1-3, Connection, Ground, Isolator | Simbol single line diagram (trafo, breaker, isolator, grounding, koneksi) |
| Pipes / Valves | Pipe* (11 jenis), ValveHorizontal, ValveVertical | Proses fluida dan perpipaan |
| Pumps / Fans | Pump 1-3, Fan1-2 | Pompa dan kipas |
| Units | Compressor, ConditionerInside/Outside, HeatExchanger1-2, Panel, UPS | Peralatan utilitas (AC, kompresor, UPS, panel) |
| Sensors | Thermometer | Suhu |
| Primitive | Ellipse, Pancake, Polygon, Polyline, PrimitiveRectangle, Rectangle | Bentuk dasar untuk menggambar sendiri |
| Containers | ConnectContainer1-2, Container | Mengelompokkan dan menghubungkan widget |

## Fitur standar di luar widget (tanpa biaya tambahan)

Event Logs (Alarm, User Login/Out, ET), Trend Lines (nilai historis), Users & Roles, iFrame, Backup & Restore, Pop-ups, Structured Tags, Mobile Layout, Widget Rotation.

## Pemetaan cepat: kebutuhan -> dashboard standar

| Kebutuhan di dashboard demo | Pakai di dashboard standar | Bisa tanpa custom HTML? |
|---|---|---|
| Angka KPI, nilai tag | Value, AnalogChip, Gauge | BISA |
| Lampu/status on-off, alarm | DiscreteLamp, DiscreteChip, Indicator | BISA |
| Grafik tren | LiveTrend, MultiLiveTrend, Trend Lines | BISA |
| Grafik batang/pie | Analytics Bar/Bars/Pie | BISA |
| Tabel data/parameter | Tables | BISA |
| Tombol kontrol, input setpoint | Command widgets | BISA (menyentuh SCADA, perlu persetujuan) |
| Single line diagram listrik | Transformer + Primitive + Connection | SEBAGIAN: simbol ada, hasil sama persis dengan desain custom perlu dicek (KONFIRMASI) |
| Proses pipa/pompa/valve | Pipes, Pumps, Valves | BISA |
| Login, role, hak akses | Users & Roles | BISA |
| Riwayat alarm/event | Event Logs, Pop-ups | BISA |
| Tampil di HP/tablet | Mobile Layout | BISA |
| Peta lokasi | widget Map atau add-on Maps/GIS | SEBAGIAN: butuh cek mana yang dipakai (KONFIRMASI) |
| Video kamera | widget VideoStream | KONFIRMASI (format stream yang didukung belum jelas) |
| Laporan siap cetak/PDF | add-on Reporting (template .mrt, Stimulsoft) | BUTUH ADD-ON |
| Kirim Telegram/e-mail | add-on Notifications | BUTUH ADD-ON |
| Rumus/logika khusus | add-on Scripting | BUTUH ADD-ON |
| Baca/tulis database lain | add-on Database Exchange | BUTUH ADD-ON |
| Data ke ERP/Power BI/app lain | add-on REST API | BUTUH ADD-ON |
| Tampilan/animasi/layout yang sangat khusus, form berbelit, logika UI custom | tidak ada widget yang setara | TIDAK, perlu custom HTML |
| Proses 24/7 di luar dashboard | tidak ada | TIDAK, perlu service |
