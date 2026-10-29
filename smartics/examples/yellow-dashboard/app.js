// Data dari SmartICS (polling), tapi ada push WebSocket, Telegram, dan export Excel tiap malam.
const rows = [];

async function load() {
  const r = await fetch("/api/v1/data/get", {
    method: "POST",
    body: JSON.stringify({ items: ["Line1.Count"] }),
  });
  const d = await r.json();
  document.getElementById("kpi").textContent = d["Line1.Count"];
  rows.push({ t: Date.now(), v: d["Line1.Count"] });
}
setInterval(load, 3000);

// Update langsung dari server (push)
const ws = new WebSocket("wss://pabrik.example.com/live");
ws.onmessage = (e) => (document.getElementById("kpi").textContent = e.data);

// Kirim ringkasan ke Telegram
document.getElementById("tg").onclick = () =>
  fetch("https://api.telegram.org/botXXXX/sendMessage", {
    method: "POST",
    body: JSON.stringify({ chat_id: "0", text: "Produksi: " + rows.length }),
  });

// Export Excel terjadwal tiap malam (jam 00:00)
function scheduleNightlyExport() {
  const now = new Date();
  const next = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1, 0, 0, 5);
  setTimeout(() => {
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, XLSX.utils.json_to_sheet(rows), "Harian");
    XLSX.writeFile(wb, "produksi-harian.xlsx");
    scheduleNightlyExport();
  }, next - now);
}
scheduleNightlyExport();
