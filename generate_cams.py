import re
import json
import requests
from pathlib import Path
from datetime import datetime

HEADERS = {"User-Agent": "Mozilla/5.0"}
WORKER_URL = "https://surfcams.polarx0.workers.dev"

CAMS = {
    "Moledo HD": {"key": "moledo", "page": "https://surftotal.com/camaras-report/minho/moledo"},
    "Vila Praia de Âncora HD": {"key": "ancora", "page": "https://surftotal.com/camaras-report/minho/vila-praia-ancora"},
    "Viana do Castelo HD": {"key": "viana_castelo", "page": "https://surftotal.com/camaras-report/minho/viana-do-castelo-hd"},
    "Ofir": {"key": "ofir", "page": "https://surftotal.com/camaras-report/minho/ofir"},

    "Aguçadoura HD": {"key": "agucadoura", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/agucadoura"},
    "Póvoa de Varzim - Ferrari HD": {"key": "ferrari", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/povoa-de-varzim-ferrari"},
    "Azurara HD": {"key": "azurara", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/azurara"},
    "Praia de Árvore - Areal HD": {"key": "arvore", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/praia-da-arvore-areal"},
    "Mindelo": {"key": "mindelo", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/mindelo"},
    "Mindelo meia laranja HD": {"key": "mindelo_meia_laranja", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/mindelo-meia-laranja"},
    "Pedras do Corgo - Melanina HD": {"key": "pedras", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/pedras-do-corgo"},
    "Cabo do Mundo HD": {"key": "cabo", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/cabo-do-mundo-hd"},
    "Leça - L'Kodak (Aterro) HD": {"key": "leca_aterro", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/leca-kodak-aterro"},
    "Leça da Palmeira HD": {"key": "leca", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/leca-da-palmeira"},
    "Matosinhos HD": {"key": "matosinhos", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/matosinhos-hd"},
    "Matosinhos - Vagas Bar HD": {"key": "vagas", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/matosinhos-vagas-bar"},
    "Cabedelo do Porto": {"key": "cabedelo", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/cabedelo-do-porto"},
    "Espinho HD": {"key": "espinho", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/espinho-hd"},
    "Espinho vista aérea HD": {"key": "espinho_aerea", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/espinho-vista-aerea"},
    "Espinho - Silvalde HD": {"key": "silvalde", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/espinho-silvalde"},

    "Cortegaça (Vila do Surf) HD": {"key": "cortegaca_vila", "page": "https://surftotal.com/camaras-report/aveiro/cortegaca-hd"},
    "Praia da Barra Norte HD": {"key": "barra_norte", "page": "https://surftotal.com/camaras-report/aveiro/praia-da-barra-norte-hd"},
    "Mira": {"key": "mira", "page": "https://surftotal.com/camaras-report/aveiro/mira"},
    "Praia do Cabedelo (Figueira da Foz)": {"key": "figueira_cabedelo", "page": "https://surftotal.com/camaras-report/figueira-da-foz/praia-do-cabedelo-hd"},
}

def now_human():
    return datetime.now().strftime("%H:%M:%S")

def find_m3u8(page_url):
    try:
        html = requests.get(page_url, headers={**HEADERS, "Referer": page_url}, timeout=20).text
        matches = re.findall(r'https?://[^"\']+?\.m3u8[^"\']*', html)
        return matches[0].replace("\\/", "/") if matches else None
    except Exception as e:
        print(f"ERROR finding stream: {page_url}: {e}")
        return None

def render_cam(name, idx, data):
    return f"""
<div class="cam" data-name={json.dumps(name)} data-key={json.dumps(data["key"])}>
  <h2>{name}</h2>
  <video id="video{idx}" controls autoplay muted playsinline preload="none"></video>
  <div class="cam-footer">
    <span class="token-info">token: loading...</span>
    <button class="refresh-icon" onclick="refreshCam('video{idx}')" title="Refresh">↻</button>
    <a href="{data["page"]}" target="_blank">Surftotal</a>
  </div>
</div>
"""

def render_offline(name, data):
    return f'<div class="offline-item"><a href="{data["page"]}" target="_blank">{name}</a></div>\n'

online_names = []
offline_names = []

for name, data in CAMS.items():
    if find_m3u8(data["page"]):
        online_names.append(name)
        print(f"{name}: ONLINE")
    else:
        offline_names.append(name)
        print(f"{name}: OFFLINE")

generated_at_human = now_human()

js = f"""
<script>
const WORKER_URL = {json.dumps(WORKER_URL)};
const hlsInstances = {{}};
const tokenTimers = {{}};
const TOKEN_LIFETIME_SECONDS = 300;
const AUTO_REFRESH_SECONDS = 270;

function fmtTime(ts) {{
  if (!ts) return "unknown";
  return new Date(ts * 1000).toLocaleTimeString();
}}

function formatDuration(seconds) {{
  const min = Math.floor(seconds / 60);
  const sec = seconds % 60;
  return min + "m " + String(sec).padStart(2, "0") + "s";
}}

function destroyCam(videoId) {{
  const video = document.getElementById(videoId);

  if (hlsInstances[videoId]) {{
    hlsInstances[videoId].destroy();
    delete hlsInstances[videoId];
  }}

  if (tokenTimers[videoId]) {{
    clearInterval(tokenTimers[videoId]);
    delete tokenTimers[videoId];
  }}

  if (video) {{
    video.pause();
    video.removeAttribute("src");
    video.load();
  }}
}}

function initCam(videoId, src) {{
  const video = document.getElementById(videoId);
  if (!video || !src) return;

  destroyCam(videoId);
  video.dataset.stream = src;
  video.muted = true;

  if (video.canPlayType("application/vnd.apple.mpegurl")) {{
    video.src = src;
    video.play().catch(() => {{}});
    return;
  }}

  if (window.Hls && Hls.isSupported()) {{
    const hls = new Hls();
    hlsInstances[videoId] = hls;
    hls.loadSource(src);
    hls.attachMedia(video);
    hls.on(Hls.Events.MANIFEST_PARSED, () => video.play().catch(() => {{}}));
  }}
}}

function updateTokenInfo(videoId, generatedAt, servedAt) {{
  const video = document.getElementById(videoId);
  const el = video?.closest(".cam")?.querySelector(".token-info");
  if (!video || !el) return;

  function tick() {{
    const now = Math.floor(Date.now() / 1000);
    const baseAge = Math.max(0, servedAt - generatedAt);
    const age = baseAge + Math.max(0, now - servedAt);
    const left = Math.max(0, TOKEN_LIFETIME_SECONDS - age);

    el.textContent =
    "⏱ " + formatDuration(left);
  }}

  tick();
  if (tokenTimers[videoId]) clearInterval(tokenTimers[videoId]);
  tokenTimers[videoId] = setInterval(tick, 1000);
}}

async function fetchFreshStream(camKey) {{
  const res = await fetch(
    WORKER_URL + "/stream?cam=" + encodeURIComponent(camKey) + "&t=" + Date.now(),
    {{ cache: "no-store" }}
  );

  const data = await res.json();
  if (!res.ok || !data.stream) throw new Error(data.error || "No stream returned");
  return data;
}}

async function startOrRefreshCam(videoId) {{
  const video = document.getElementById(videoId);
  const card = video?.closest(".cam");
  const camKey = card?.dataset.key;
  const el = card?.querySelector(".token-info");
  if (!video || !camKey) return;

  try {{
    if (el) el.textContent = "token: loading...";
    const data = await fetchFreshStream(camKey);
    const now = Math.floor(Date.now() / 1000);
    initCam(videoId, data.stream);
    updateTokenInfo(videoId, data.generatedAt || now, data.servedAt || now);
  }} catch (e) {{
    console.error(e);
    if (el) el.textContent = "token: failed to load";
  }}
}}

async function refreshCam(videoId) {{
  await startOrRefreshCam(videoId);
}}

async function refreshAll() {{
  for (const video of Array.from(document.querySelectorAll(".cam video"))) {{
    await startOrRefreshCam(video.id);
  }}
}}

function stopAll() {{
  document.querySelectorAll("video").forEach(video => {{
    destroyCam(video.id);
    const el = video.closest(".cam")?.querySelector(".token-info");
    if (el) el.textContent = "stopped";
  }});
}}

window.addEventListener("load", () => {{
  refreshAll();
  setInterval(refreshAll, AUTO_REFRESH_SECONDS * 1000);
}});
</script>
"""

html = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Norte Surf Cams</title>
<script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
{js}
<style>
body {{ margin:0; font-family:Arial,sans-serif; background:#111; color:#eee; }}
header {{ padding:10px 12px; background:#1b1b1b; position:sticky; top:0; z-index:10; }}
button {{ margin:4px; padding:7px 10px; cursor:pointer; border-radius:6px; border:0; }}
.refresh-icon {{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  width:22px;
  height:22px;
  padding:0;
  margin:0;
  border:0;
  background:transparent;
  color:#8ecbff;
  font-size:18px;
  font-weight:bold;
  cursor:pointer;
  flex-shrink:0;
}}
.grid {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:8px; padding:8px; }}
.cam {{ background:#222; border-radius:10px; overflow:hidden; }}
.cam h2 {{ margin:0; padding:8px 10px; font-size:14px; line-height:1.2; }}
video {{ width:100%; background:#000; display:block; min-height:120px; }}
.cam-footer {{
  display:flex;
  align-items:center;
  gap:6px;
  padding:7px 10px 9px;
  font-size:12px;
  white-space:nowrap;
  overflow-x:auto;
}}
.token-info {{ color:#ddd; flex-shrink:0; }}
a {{ color:#8ecbff; flex-shrink:0; }}
.bad {{ padding:12px; color:#ffb3b3; }}
.offline-list {{ padding:0 12px 20px; }}
.offline-item {{ padding:8px 10px; background:#222; margin-bottom:6px; border-radius:8px; }}
@media (max-width:600px) {{
  .grid {{ grid-template-columns:repeat(2,minmax(0,1fr)); gap:6px; padding:6px; }}
  .cam h2 {{ font-size:11px; padding:6px 7px; }}
  .cam-footer {{ font-size:10px; gap:4px; flex-wrap:nowrap; }}
  .refresh-icon {{ width:18px; height:18px; font-size:14px; }}
  video {{ min-height:90px; }}
}}
</style>
</head>
<body>

<header>
  <b>Norte Surf Cams</b><br>
  <span>
    page generated: {generated_at_human}
    | 🟢 {len(online_names)} online
    | 🔴 {len(offline_names)} offline
  </span><br>
  <button onclick="refreshAll()">Refresh All</button>
  <button onclick="stopAll()">Stop All</button>
</header>

<h2 style="padding-left:12px">🌊 Online Cameras</h2>
"""

if online_names:
    html += '<div class="grid">\n'
    for idx, name in enumerate(online_names):
        html += render_cam(name, idx, CAMS[name])
    html += "</div>\n"
else:
    html += '<div class="bad">No cameras are currently online.</div>\n'

html += """
<h2 style="padding-left:12px">⚠️ Offline / unavailable</h2>
<div class="offline-list">
"""

for name in offline_names:
    html += render_offline(name, CAMS[name])

html += """
<hr style="margin:20px 12px;border-color:#333">

<div style="
  padding:12px;
  font-size:12px;
  color:#999;
  text-align:center;
">
  Surf camera streams and camera information are provided by
  <a href="https://surftotal.com" target="_blank">Surftotal</a>.
  Please visit the original website for full surf reports, forecasts and camera access.
</div>

</body>
</html>
"""

Path("cams.html").write_text(html, encoding="utf-8")
print("Generated: cams.html")
print(f"Online: {len(online_names)}")
print(f"Offline: {len(offline_names)}")
print(f"Page generated: {generated_at_human}")
