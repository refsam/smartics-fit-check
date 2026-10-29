// Dashboard demo: data asli lewat Public API SmartICS (same origin), polling 2 detik.
const TAGS = ["Plant.Tank1.Level", "Plant.Tank1.Temp"];
const history = [];

async function login(user, pass) {
  const r = await fetch("/api/user/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username: user, password: pass }),
  });
  return r.ok;
}

async function poll() {
  const r = await fetch("/api/v1/data/get", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ items: TAGS }),
  });
  if (r.status === 401) {
    document.getElementById("login").hidden = false;
    return;
  }
  const data = await r.json();
  document.getElementById("level").textContent = data[TAGS[0]];
  document.getElementById("temp").textContent = data[TAGS[1]];
  history.push(data[TAGS[0]]);
  if (history.length > 30) history.shift();
}

document.getElementById("login").addEventListener("submit", async (e) => {
  e.preventDefault();
  if (await login(u.value, p.value)) location.reload();
});

setInterval(poll, 2000);
poll();
