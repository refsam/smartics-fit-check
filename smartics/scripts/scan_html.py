#!/usr/bin/env python3
"""Scanner statis untuk dashboard custom HTML (skill /smartics).

Hanya MENDETEKSI pola sesuai daftar cek di references/scoring-rubric.md bagian 5.2.
Tidak memutuskan status/persen (itu tugas Claude), tidak membuat panggilan jaringan,
tidak mengubah file input. Nilai secret selalu disamarkan pada output.

Pemakaian:
    python scan_html.py <file.html | folder | file.zip> [--pretty]
"""
import argparse
import json
import re
import sys
import tempfile
import zipfile
from pathlib import Path

MAX_FILE_BYTES = 2 * 1024 * 1024
TEXT_EXTS = {".html", ".htm", ".js", ".mjs", ".css", ".json"}
SERVER_EXTS = {".php", ".py", ".asp", ".aspx", ".cshtml", ".jsp", ".rb"}
SKIP_DIRS = {"node_modules", ".git", "__pycache__"}
LIB_DIRS = {"lib", "libs", "vendor", "vendors", "third_party"}
MAX_PER_CHECK_PER_FILE = 20
MAX_EVIDENCE = 160

LABELS = {
    1: "Resource eksternal (CDN/font/gambar)",
    2: "Panggilan SmartICS API",
    3: "Panggilan ke URL absolut luar",
    4: "WebSocket/EventSource/MQTT di browser",
    5: "Data dummy/mock",
    6: "Form login buatan sendiri",
    7: "Secret/kredensial di kode",
    8: "Video/RTSP/HLS",
    9: "Kamera/mikrofon/push to talk",
    10: "Peta",
    11: "Chart/3D",
    12: "Export PDF/Excel/print dari browser",
    13: "Kirim e-mail/Telegram/WhatsApp",
    14: "Sinkron ke cloud/ERP/sistem lain",
    15: "Koneksi database/SQL di front-end",
    16: "Penanda kode server-side",
    17: "Framework dengan build step",
    18: "Proses latar/penjadwalan di browser",
    19: "Upload file/tulis file",
    20: "Koneksi langsung ke PLC/driver",
    21: "Tulis ke tag (item/set)",
    22: "Redundancy",
}

# Library: (nama, check, regex)
LIBRARIES = [
    ("Chart.js", 11, r"chart(?:\.umd)?(?:\.min)?\.js|new\s+Chart\s*\(|Chart\.js"),
    ("ECharts", 11, r"echarts"),
    ("three.js", 11, r"three(?:\.module)?(?:\.min)?\.js|\bTHREE\.|from\s+['\"]three['\"]"),
    ("Leaflet", 10, r"leaflet|\bL\.map\s*\("),
    ("Google Maps", 10, r"maps\.googleapis\.com|google\.maps\."),
    ("jsPDF", 12, r"jspdf|jsPDF"),
    ("SheetJS", 12, r"xlsx(?:\.full)?(?:\.min)?\.js|XLSX\.(?:utils|writeFile|write)|sheetjs"),
    ("React", 17, r"react(?:-dom)?(?:\.production)?(?:\.min)?\.js|from\s+['\"]react['\"]|ReactDOM"),
    ("Vue", 17, r"vue(?:\.global)?(?:\.min)?\.js|\bcreateApp\s*\(|new\s+Vue\s*\("),
    ("MQTT.js", 4, r"mqtt(?:\.min)?\.js|mqtt\.connect"),
    ("axios", None, r"axios"),
]

LOCAL_HOST = re.compile(r"^(?:https?:)?//(?:localhost|127\.0\.0\.1|\[::1\])(?:[:/]|$)", re.I)

# Pola per-baris: (check, label tambahan, regex, flags)
LINE_PATTERNS = []


def _p(check, label, rx, flags=re.I):
    LINE_PATTERNS.append((check, label, re.compile(rx, flags)))


_p(1, "script/link/img/iframe eksternal",
   r"<(?:script|link|img|source|iframe)\b[^>]*?(?:src|href)\s*=\s*[\"']((?:https?:)?//[^\"']+)")
_p(1, "url() / @import eksternal di CSS",
   r"(?:url\(\s*[\"']?|@import\s+[\"']?)((?:https?:)?//[^)\"'\s]+)")
_p(3, "fetch/axios/XHR ke URL absolut",
   r"(?:fetch|axios(?:\.\w+)?|\.open|\$\.(?:get|post|ajax))\s*\(\s*(?:[\"'][A-Za-z]+[\"']\s*,\s*)?[\"'`](https?://[^\"'`\s]+)")
_p(4, "WebSocket", r"new\s+WebSocket\s*\(|\bwss?://")
_p(4, "EventSource (SSE)", r"new\s+EventSource\s*\(")
_p(5, "Math.random", r"Math\.random\s*\(")
_p(5, "array angka hardcode",
   r"\[\s*-?\d+(?:\.\d+)?(?:\s*,\s*-?\d+(?:\.\d+)?){5,}\s*\]", 0)
_p(6, "input password / form login", r"type\s*=\s*[\"']password[\"']")
_p(7, "kredensial di URL",
   r"[a-z][a-z0-9+.-]*://[^/\s:@\"']+:[^/\s@\"']+@")
_p(7, "password/key/token hardcode",
   r"(?:password|passwd|pwd|secret|api[_-]?key|apikey|access[_-]?key|auth[_-]?token|token)[\"']?\s*[:=]\s*[\"'][^\"'\s]{4,}[\"']")
_p(7, "Bearer token", r"Bearer\s+[A-Za-z0-9._\-]{16,}")
_p(7, "pola key cloud", r"\b(?:AKIA[0-9A-Z]{16}|sk-[A-Za-z0-9]{20,})\b", 0)
_p(8, "tag <video>", r"<video\b")
_p(8, "RTSP", r"rtsp://")
_p(8, "HLS", r"\.m3u8|hls\.js|new\s+Hls\s*\(")
_p(9, "getUserMedia/MediaRecorder", r"getUserMedia|MediaRecorder|push[\s_-]?to[\s_-]?talk|walkie")
_p(10, "peta (Google Maps API)", r"maps\.googleapis\.com")
_p(12, "print dari browser", r"window\.print\s*\(")
_p(13, "Telegram", r"api\.telegram\.org|\btelegram\b")
_p(13, "WhatsApp", r"wa\.me/|api\.whatsapp|\bwhatsapp\b")
_p(13, "SMTP/e-mail", r"\bsmtp\b|nodemailer|sendmail|emailjs")
_p(14, "cloud/ERP", r"firebase|amazonaws\.com|azurewebsites|supabase|\berp\b|odoo|sap\.com")
_p(15, "connection string / driver DB",
   r"(?:Server|Data Source|Host)\s*=[^;\"']+;[^\"']*(?:Database|Initial Catalog)\s*=|(?:mysql|postgres(?:ql)?|mongodb|mssql|sqlserver)://|createConnection\s*\(|new\s+mysqli|new\s+PDO\s*\(|new\s+Pool\s*\(|mssql\.connect|\bmysql\.")
_p(15, "SQL di JS (aman bila lewat /api/v1/database/query dengan Alias)",
   r"[\"'`]\s*(?:SELECT\s.+?\sFROM\s|INSERT\s+INTO\s|UPDATE\s+\w+\s+SET\s|DELETE\s+FROM\s)")
_p(16, "kode server-side", r"<\?php|<%@|\brequire\s*\(|\bexpress\s*\(|from\s+flask|\bFlask\s*\(|\.listen\s*\(")
_p(18, "setInterval", r"setInterval\s*\(")
_p(18, "kata kunci penjadwalan", r"\bcron\b|nightly|terjadwal|tiap\s+malam|scheduled?\b", re.I)
_p(19, "upload/tulis file", r"type\s*=\s*[\"']file[\"']|new\s+FormData|showSaveFilePicker|fs\.write\w*")
_p(20, "protokol device langsung", r"modbus|opc\.tcp|opcua|snap7|s7comm|ethernet/ip")
_p(21, "tulis tag", r"/api/v1/item/set")
_p(22, "redundancy", r"redundan")

API_RX = re.compile(r"/api/(?:v1/[A-Za-z0-9_/]+|user/[A-Za-z0-9_]+)")
EXT_URL_RX = re.compile(r"(?:https?:)?//[A-Za-z0-9.\-]+(?::\d+)?(?:/[^\s\"'`)<>]*)?")

# ---------- penyamaran ----------
_RE_URL_CRED = re.compile(r"([a-z][a-z0-9+.-]*://)([^/\s:@\"']+):([^/\s@\"']+)@(\d{1,3}\.\d{1,3})\.\d{1,3}\.\d{1,3}", re.I)
_RE_URL_CRED_ANY = re.compile(r"([a-z][a-z0-9+.-]*://)([^/\s:@\"']+):([^/\s@\"']+)@", re.I)
_RE_KV = re.compile(
    r"((?:password|passwd|pwd|secret|api[_-]?key|apikey|access[_-]?key|auth[_-]?token|token)[\"']?\s*[:=]\s*[\"'])([^\"'\s]{4,})([\"'])",
    re.I)
_RE_BEARER = re.compile(r"(Bearer\s+)[A-Za-z0-9._\-]{16,}")
_RE_CLOUDKEY = re.compile(r"\b(?:AKIA[0-9A-Z]{16}|sk-[A-Za-z0-9]{20,})\b")
_RE_CONN_PW = re.compile(r"((?:Password|Pwd)\s*=)[^;\"']+", re.I)


_RE_MYSQLI = re.compile(r"(new\s+mysqli\s*\(\s*[\"'][^\"']*[\"']\s*,\s*[\"'][^\"']*[\"']\s*,\s*)[\"'][^\"']*[\"']", re.I)


def redact(text):
    text = _RE_MYSQLI.sub(lambda m: m.group(1) + '"****"', text)
    text = _RE_URL_CRED.sub(lambda m: f"{m.group(1)}{m.group(2)}:****@{m.group(4)}.x.x", text)
    text = _RE_URL_CRED_ANY.sub(lambda m: f"{m.group(1)}{m.group(2)}:****@", text)
    text = _RE_KV.sub(lambda m: f"{m.group(1)}****{m.group(3)}", text)
    text = _RE_BEARER.sub(lambda m: f"{m.group(1)}****", text)
    text = _RE_CLOUDKEY.sub("****", text)
    text = _RE_CONN_PW.sub(lambda m: f"{m.group(1)}****", text)
    return text


def evidence(line):
    line = redact(line.strip())
    if len(line) > MAX_EVIDENCE:
        line = line[:MAX_EVIDENCE] + "..."
    return line


# ---------- pengumpulan file ----------
def is_library_file(rel):
    parts = {p.lower() for p in rel.parts[:-1]}
    name = rel.name.lower()
    return bool(parts & LIB_DIRS) or ".min." in name


def collect(root):
    if root.is_file():
        return [(root, Path(root.name))]
    out = []
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(root)
        if SKIP_DIRS & set(rel.parts):
            continue
        out.append((p, rel))
    return out


def extract_zip(zpath, dest):
    with zipfile.ZipFile(zpath) as z:
        base = dest.resolve()
        for m in z.namelist():
            target = (dest / m).resolve()
            if base != target and base not in target.parents:
                raise ValueError(f"zip tidak aman (path keluar folder): {m}")
        z.extractall(dest)


# ---------- scan ----------
def scan(root):
    findings, libraries, api, ext_urls = [], {}, set(), set()
    scanned = 0

    def add(check, label, rel, line, ev, counts):
        key = (check, str(rel))
        counts[key] = counts.get(key, 0) + 1
        if counts[key] > MAX_PER_CHECK_PER_FILE:
            return
        findings.append({"check": check, "label": f"{LABELS[check]}: {label}" if label else LABELS[check],
                         "file": str(rel).replace("\\", "/"), "line": line, "evidence": ev})

    counts = {}
    for path, rel in collect(root):
        ext = path.suffix.lower()
        if ext in SERVER_EXTS:
            add(16, f"file server-side ({ext})", rel, 0, rel.name, counts)
            continue
        if ext not in TEXT_EXTS:
            continue
        try:
            if path.stat().st_size > MAX_FILE_BYTES:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        scanned += 1
        lib_file = is_library_file(rel)

        # library dari nama file / isi
        for name, check, rx in LIBRARIES:
            hit = re.search(rx, rel.name, re.I) if lib_file else None
            if hit and name not in libraries:
                libraries[name] = str(rel).replace("\\", "/")
        if lib_file:
            continue  # jangan scan isi library (banyak false positive)

        seen_lib = set()
        for ln, line in enumerate(text.splitlines(), 1):
            if len(line) > 5000:  # kemungkinan minified
                continue
            for name, check, rx in LIBRARIES:
                if name in seen_lib:
                    continue
                if re.search(rx, line, re.I):
                    seen_lib.add(name)
                    libraries.setdefault(name, str(rel).replace("\\", "/"))
                    if check:
                        add(check, name, rel, ln, evidence(line), counts)
            for m in API_RX.finditer(line):
                api.add(m.group(0))
            for check, label, rx in LINE_PATTERNS:
                m = rx.search(line)
                if not m:
                    continue
                if check == 1:
                    url = m.group(1)
                    if LOCAL_HOST.match(url):
                        continue
                    ext_urls.add(redact(url))
                if check == 3 and LOCAL_HOST.match(m.group(1)):
                    continue
                if check == 3:
                    ext_urls.add(redact(m.group(1)))
                if check == 4 and label == "WebSocket" and "wss://" not in line.lower() \
                        and "ws://" not in line.lower() and "WebSocket(" not in line:
                    continue
                add(check, label, rel, ln, evidence(line), counts)
            if API_RX.search(line):
                add(2, "", rel, ln, evidence(line), counts)

    return {
        "files_scanned": scanned,
        "findings": sorted(findings, key=lambda f: (f["check"], f["file"], f["line"])),
        "libraries": sorted(libraries),
        "library_files": libraries,
        "endpoints": {"smartics_api": sorted(api), "external_urls": sorted(ext_urls)},
    }


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Scanner statis dashboard custom HTML untuk skill /smartics. "
                    "Output JSON ke stdout. Tidak ada panggilan jaringan; file input tidak diubah.")
    ap.add_argument("path", help="file .html, folder, atau .zip")
    ap.add_argument("--pretty", action="store_true", help="JSON dengan indentasi")
    args = ap.parse_args(argv)

    src = Path(args.path)
    if not src.exists():
        print(f"Error: path tidak ditemukan: {src}", file=sys.stderr)
        return 2
    try:
        if src.is_file() and src.suffix.lower() == ".zip":
            with tempfile.TemporaryDirectory(prefix="smartics_scan_") as tmp:
                extract_zip(src, Path(tmp))
                result = scan(Path(tmp))
        else:
            result = scan(src)
    except zipfile.BadZipFile:
        print(f"Error: bukan file zip yang valid: {src}", file=sys.stderr)
        return 2
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2 if args.pretty else None)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
