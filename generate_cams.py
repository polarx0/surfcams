import re
import json
import requests
from pathlib import Path

HEADERS = {"User-Agent": "Mozilla/5.0"}
WORKER_URL = "https://surfcams.polarx0.workers.dev"

CAMS = {
    "Moledo HD": {"key": "moledo", "page": "https://surftotal.com/camaras-report/minho/moledo", "stars": "★★★★☆"},
    "Vila Praia de Âncora HD": {"key": "ancora", "page": "https://surftotal.com/camaras-report/minho/vila-praia-ancora", "stars": "★★★☆☆"},
    "Viana do Castelo HD": {"key": "viana_castelo", "page": "https://surftotal.com/camaras-report/minho/viana-do-castelo-hd", "stars": "★★★☆☆"},
    "Ofir": {"key": "ofir", "page": "https://surftotal.com/camaras-report/minho/ofir", "stars": "★★★★☆"},

    "Aguçadoura HD": {"key": "agucadoura", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/agucadoura", "stars": "★★★☆☆"},
    "Póvoa de Varzim - Ferrari HD": {"key": "ferrari", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/povoa-de-varzim-ferrari", "stars": "★★☆☆☆"},
    "Azurara HD": {"key": "azurara", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/azurara", "stars": "★★★☆☆"},
    "Praia de Árvore - Areal HD": {"key": "arvore", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/praia-da-arvore-areal", "stars": "★★★☆☆"},
    "Mindelo": {"key": "mindelo", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/mindelo", "stars": "★★☆☆☆"},
    "Mindelo meia laranja HD": {"key": "mindelo_meia_laranja", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/mindelo-meia-laranja", "stars": "★★☆☆☆"},
    "Pedras do Corgo - Melanina HD": {"key": "pedras", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/pedras-do-corgo", "stars": "★★☆☆☆"},
    "Cabo do Mundo HD": {"key": "cabo", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/cabo-do-mundo-hd", "stars": "★★☆☆☆"},
    "Leça - L'Kodak (Aterro) HD": {"key": "leca_aterro", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/leca-kodak-aterro", "stars": "★★☆☆☆"},
    "Leça da Palmeira HD": {"key": "leca", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/leca-da-palmeira", "stars": "★★☆☆☆"},
    "Matosinhos HD": {"key": "matosinhos", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/matosinhos-hd", "stars": "★★☆☆☆"},
    "Matosinhos - Vagas Bar HD": {"key": "vagas", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/matosinhos-vagas-bar", "stars": "★★★☆☆"},
    "Cabedelo do Porto": {"key": "cabedelo", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/cabedelo-do-porto", "stars": "★★☆☆☆"},
    "Espinho HD": {"key": "espinho", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/espinho-hd", "stars": "★★★☆☆"},
    "Espinho vista aérea HD": {"key": "espinho_aerea", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/espinho-vista-aerea", "stars": "★★★☆☆"},
    "Espinho - Silvalde HD": {"key": "silvalde", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/espinho-silvalde", "stars": "★★★★☆"},

    "Cortegaça (Vila do Surf) HD": {"key": "cortegaca_vila", "page": "https://surftotal.com/camaras-report/aveiro/cortegaca-hd", "stars": "★★★☆☆"},
    "Praia da Barra Norte HD": {"key": "barra_norte", "page": "https://surftotal.com/camaras-report/aveiro/praia-da-barra-norte-hd", "stars": "★★★☆☆"},
    "Mira": {"key": "mira", "page": "https://surftotal.com/camaras-report/aveiro/mira", "stars": "★★★☆☆"},
    "Praia do Cabedelo (Figueira da Foz)": {"key": "figueira_cabedelo", "page": "https://surftotal.com/camaras-report/figueira-da-foz/praia-do-cabedelo-hd", "stars": "★★★☆☆"},
}

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
    <span class="token-info">⏱ loading</span>
    <span class="sep">|</span>
    <button class="forecast-pill" onclick="showForecast('{data["key"]}')" title="Forecast">☆☆☆☆☆</button>
    <span class="sep">|</span>
    <button class="energy-pill" onclick="showForecast('{data["key"]}')" title="Forecast energy">-- kJ</button>
    <span class="sep">|</span>
    <span class="wind-pill">-- m/s</span>
    <span class="sep">|</span>
    <button class="refresh-icon" onclick="refreshCam('video{idx}')" title="Refresh">↻</button>
    <span class="sep">|</span>
    <a class="source-link" href="{data["page"]}" target="_blank">Surftotal</a>
  </div>
</div>
"""

def render_offline(name, data):
    return f"""
<div class="offline-item">
  <span>{name}</span>
  <span class="sep">|</span>
  <a href="{data["page"]}" target="_blank">Surftotal</a>
</div>
"""

online_names = []
offline_names = []

for name, data in CAMS.items():
    if find_m3u8(data["page"]):
        online_names.append(name)
        print(f"{name}: ONLINE")
    else:
        offline_names.append(name)
        print(f"{name}: OFFLINE")

js = f"""
<script>
const WORKER_URL = {json.dumps(WORKER_URL)};
const hlsInstances = {{}};
const tokenTimers = {{}};
const forecastCache = {{}};
const TOKEN_LIFETIME_SECONDS = 300;
const AUTO_REFRESH_SECONDS = 270;

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
    el.textContent = "⏱ " + formatDuration(left);
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
    if (el) el.textContent = "⏱ loading";
    const data = await fetchFreshStream(camKey);
    const now = Math.floor(Date.now() / 1000);
    initCam(videoId, data.stream);
    updateTokenInfo(videoId, data.generatedAt || now, data.servedAt || now);
  }} catch (e) {{
    console.error(e);
    if (el) el.textContent = "⏱ failed";
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


async function fetchForecast(spotKey) {{
  const res = await fetch(
    WORKER_URL + "/forecast?spot=" + encodeURIComponent(spotKey) + "&t=" + Date.now(),
    {{ cache: "no-store" }}
  );

  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Forecast failed");

  forecastCache[spotKey] = data;
  return data;
}}

function updateForecastInCard(card, data) {{
  const starsEl = card.querySelector(".forecast-pill");
  const energyEl = card.querySelector(".energy-pill");
  const windEl = card.querySelector(".wind-pill");

  if (starsEl) starsEl.textContent = data.stars || "☆☆☆☆☆";
  if (energyEl) energyEl.textContent = (data.energyKj ?? "--") + " kJ";
  if (windEl) windEl.textContent = ((data.wind && data.wind.speedMs != null) ? data.wind.speedMs : "--") + " m/s";
}}

async function loadForecastForCard(card) {{
  const spotKey = card?.dataset.key;
  if (!spotKey) return;

  try {{
    const data = await fetchForecast(spotKey);
    updateForecastInCard(card, data);
  }} catch (e) {{
    console.error(e);
    const starsEl = card.querySelector(".forecast-pill");
    const energyEl = card.querySelector(".energy-pill");
    const windEl = card.querySelector(".wind-pill");
    if (starsEl) starsEl.textContent = "☆☆☆☆☆";
    if (energyEl) energyEl.textContent = "-- kJ";
    if (windEl) windEl.textContent = "-- m/s";
  }}
}}

async function loadAllForecasts() {{
  const cards = Array.from(document.querySelectorAll(".cam"));
  for (const card of cards) {{
    await loadForecastForCard(card);
  }}
}}

async function showForecast(spotKey) {{
  let data = forecastCache[spotKey];

  if (!data) {{
    const card = document.querySelector('.cam[data-key="' + spotKey + '"]');
    await loadForecastForCard(card);
    data = forecastCache[spotKey];
  }}

  if (!data) return;

  const text =
    data.name + "\\n\\n" +
    (data.stars || "☆☆☆☆☆") + "\\n\\n" +
    "Energy: " + (data.energyKj ?? "--") + " kJ\\n\\n" +
    "Wave: " + fmt(data.wave?.heightM, " m") +
    " @ " + fmt(data.wave?.periodS, " s") +
    " " + (data.wave?.directionText || "") + "\\n" +
    "Swell: " + fmt(data.swell?.heightM, " m") +
    " @ " + fmt(data.swell?.periodS, " s") +
    " " + (data.swell?.directionText || "") + "\\n\\n" +
    "Wind: " + fmt(data.wind?.speedMs, " m/s") +
    " " + (data.wind?.directionText || "") + "\\n" +
    "Effect: " + (data.wind?.effect || "unknown") + "\\n\\n" +
    "Tide: " + (data.tide?.state || "unknown") + "\\n" +
    "Updated: " + (data.updatedLocal || "unknown");

  alert(text);
}}

function fmt(value, suffix) {{
  return value == null ? "--" : value + suffix;
}}

window.addEventListener("load", () => {{
  refreshAll();
  loadAllForecasts();
  setInterval(refreshAll, AUTO_REFRESH_SECONDS * 1000);
  setInterval(loadAllForecasts, 60 * 60 * 1000);
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

.header-bar {{
  display:flex;
  align-items:center;
  justify-content:flex-start;
  gap:4px;
  padding:10px 12px;
  background:#1b1b1b;
  position:sticky;
  top:0;
  z-index:10;
}}

.header-line {{
  color:#ddd;
  font-size:14px;
  white-space:nowrap;
}}

.refresh-all-icon {{
  width:20px;
  height:20px;
  padding:0;
  border:0;
  background:transparent;
  color:#8ecbff;
  font-size:18px;
  cursor:pointer;
}}

.grid {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:8px; padding:8px; }}
.cam {{ background:#222; border-radius:10px; overflow:hidden; }}
.cam h2 {{ margin:0; padding:8px 10px; font-size:14px; line-height:1.2; }}
video {{ width:100%; background:#000; display:block; min-height:120px; }}

.cam-footer {{
  display:flex;
  align-items:center;
  justify-content:flex-start;
  gap:4px;
  padding:7px 8px;
  font-size:11px;
  white-space:nowrap;
}}

.sep {{ color:#666; flex-shrink:0; }}
.token-info {{ color:#ddd; flex-shrink:0; }}
.wind-pill {{ color:#ddd; flex-shrink:0; }}
.forecast-pill,
.energy-pill {{
  padding:0;
  margin:0;
  border:0;
  background:transparent;
  color:#ffd36a;
  font:inherit;
  cursor:pointer;
  flex-shrink:0;
}}
.energy-pill {{ color:#ddd; }}

.refresh-icon {{
  width:14px;
  height:14px;
  padding:0;
  border:0;
  background:transparent;
  color:#8ecbff;
  font-size:13px;
  cursor:pointer;
  flex-shrink:0;
}}

.source-link {{
  color:#8ecbff;
  text-decoration:none;
  flex-shrink:0;
}}

a {{ color:#8ecbff; }}
.bad {{ padding:12px; color:#ffb3b3; }}

.offline-list {{ padding:0 12px 20px; }}
.offline-item {{
  display:flex;
  align-items:center;
  gap:6px;
  padding:8px 10px;
  background:#222;
  margin-bottom:6px;
  border-radius:8px;
  font-size:12px;
}}

.footer-credit {{
  padding:12px;
  font-size:12px;
  color:#999;
  text-align:center;
}}

@media (max-width:600px) {{
  .header-line {{ font-size:11px; }}
  .refresh-all-icon {{ width:18px; height:18px; font-size:15px; }}

  .grid {{ grid-template-columns:repeat(2,minmax(0,1fr)); gap:6px; padding:6px; }}
  .cam h2 {{ font-size:11px; padding:6px 7px; }}
  .cam-footer {{ font-size:9px; gap:3px; padding:6px 5px; }}
  .refresh-icon {{ width:12px; height:12px; font-size:11px; }}
  .source-link {{ font-size:9px; }}
  video {{ min-height:90px; }}
}}
</style>
</head>
<body>

<header class="header-bar">
  <span class="header-line">Norte Surf Cams | 🟢 {len(online_names)} online | 🔴 {len(offline_names)} offline |</span>
  <button class="refresh-all-icon" onclick="refreshAll()" title="Refresh all">↻</button>
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
<h2 style="padding-left:12px">⚠️ Offline Cameras</h2>
<div class="offline-list">
"""

for name in offline_names:
    html += render_offline(name, CAMS[name])

html += """
</div>

<hr style="margin:20px 12px;border-color:#333">

<div class="footer-credit">
  Camera data courtesy of
  <a href="https://surftotal.com" target="_blank">Surftotal</a>.
</div>

</body>
</html>
"""

Path("cams.html").write_text(html, encoding="utf-8")
print("Generated: cams.html")
print(f"Online: {len(online_names)}")
print(f"Offline: {len(offline_names)}")
