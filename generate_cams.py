import re
import json
import requests
from pathlib import Path

HEADERS = {"User-Agent": "Mozilla/5.0"}
REQUEST_TIMEOUT_SECONDS = 8
WORKER_URL = "https://surfcams.polarx0.workers.dev"

CAMS = {
    "Moledo HD": {"key": "moledo", "page": "https://surftotal.com/camaras-report/minho/moledo", "stars": "★★★★☆"},
    "Vila Praia de Âncora HD": {"key": "ancora", "page": "https://surftotal.com/camaras-report/minho/vila-praia-ancora", "stars": "★★★☆☆"},
    "Vila Praia de Âncora | Beachcam": {"key": "bc_ancora", "forecast_key": "ancora", "source": "beachcam", "page": "https://beachcam.meo.pt/livecams/vila-praia-de-ancora/", "stars": "★★★☆☆"},
    "Viana do Castelo HD": {"key": "viana_castelo", "page": "https://surftotal.com/camaras-report/minho/viana-do-castelo-hd", "stars": "★★★☆☆"},
    "Viana do Castelo | Cabedelo": {"key": "bc_viana_cabedelo", "forecast_key": "viana_castelo", "source": "beachcam", "page": "https://beachcam.meo.pt/livecams/viana-do-castelo-cabedelo/", "stars": "★★★☆☆"},
    "Esposende": {"key": "bc_esposende", "forecast_key": "ofir", "source": "beachcam", "page": "https://beachcam.meo.pt/livecams/esposende/", "stars": "★★★☆☆"},
    "Esposende | Foz do Cávado": {"key": "bc_esposende_foz", "forecast_key": "ofir", "source": "beachcam", "page": "https://beachcam.meo.pt/livecams/esposende-foz-do-cavado/", "stars": "★★★☆☆"},
    "Ofir | Beachcam": {"key": "bc_ofir", "forecast_key": "ofir", "source": "beachcam", "page": "https://beachcam.meo.pt/livecams/ofir/", "stars": "★★★☆☆"},
    "Ofir": {"key": "ofir", "page": "https://surftotal.com/camaras-report/minho/ofir", "stars": "★★★★☆"},
    "Apúlia": {"key": "bc_apulia", "forecast_key": "ofir", "source": "beachcam", "page": "https://beachcam.meo.pt/livecams/apulia/", "stars": "★★★☆☆"},

    "Aguçadoura HD": {"key": "agucadoura", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/agucadoura", "stars": "★★★☆☆"},
    "Póvoa de Varzim - Ferrari HD": {"key": "ferrari", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/povoa-de-varzim-ferrari", "stars": "★★☆☆☆"},
    "Vila do Conde | Caxinas": {"key": "bc_caxinas", "forecast_key": "azurara", "source": "beachcam", "page": "https://beachcam.meo.pt/livecams/caxinas-macaco-17/", "stars": "★★★☆☆"},
    "Azurara HD": {"key": "azurara", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/azurara", "stars": "★★★☆☆"},
    "Praia de Árvore - Areal HD": {"key": "arvore", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/praia-da-arvore-areal", "stars": "★★★☆☆"},
    "Mindelo": {"key": "mindelo", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/mindelo", "stars": "★★☆☆☆"},
    "Mindelo meia laranja HD": {"key": "mindelo_meia_laranja", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/mindelo-meia-laranja", "stars": "★★☆☆☆"},
    "Pedras do Corgo - Melanina HD": {"key": "pedras", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/pedras-do-corgo", "stars": "★★☆☆☆"},
    "Cabo do Mundo HD": {"key": "cabo", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/cabo-do-mundo-hd", "stars": "★★☆☆☆"},
    "Leça - L'Kodak (Aterro) HD": {"key": "leca_aterro", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/leca-kodak-aterro", "stars": "★★☆☆☆"},
    "Leça da Palmeira | Panorâmica Aterro": {"key": "bc_leca_aterro", "forecast_key": "leca_aterro", "source": "beachcam", "page": "https://beachcam.meo.pt/livecams/leca-da-palmeira-panoraminca-aterro/", "stars": "★★★☆☆"},
    "Leça da Palmeira HD": {"key": "leca", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/leca-da-palmeira", "stars": "★★☆☆☆"},
    "Leça da Palmeira | Beachcam": {"key": "bc_leca", "forecast_key": "leca", "source": "beachcam", "page": "https://beachcam.meo.pt/livecams/leca-da-palmeira/", "stars": "★★★☆☆"},
    "Matosinhos | Beachcam": {"key": "bc_matosinhos", "forecast_key": "matosinhos", "source": "beachcam", "page": "https://beachcam.meo.pt/livecams/praia-de-matosinhos/", "stars": "★★★☆☆"},
    "Matosinhos HD": {"key": "matosinhos", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/matosinhos-hd", "stars": "★★☆☆☆"},
    "Matosinhos - Vagas Bar HD": {"key": "vagas", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/matosinhos-vagas-bar", "stars": "★★★☆☆"},
    "Porto | Homem do Leme": {"key": "bc_homem_do_leme", "forecast_key": "matosinhos", "source": "beachcam", "page": "https://beachcam.meo.pt/livecams/porto-homem-do-leme/", "stars": "★★★☆☆"},
    "Porto | Carneiro": {"key": "bc_carneiro", "forecast_key": "matosinhos", "source": "beachcam", "page": "https://beachcam.meo.pt/livecams/porto-carneiro/", "stars": "★★★☆☆"},
    "Cabedelo do Porto": {"key": "cabedelo", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/cabedelo-do-porto", "stars": "★★☆☆☆"},
    "Praia Canide Norte/Sul": {"key": "canide", "forecast_key": "cabedelo", "source": "beachcam", "page": "https://beachcam.meo.pt/livecams/praia-canide-norte-sul/", "stars": "★★★☆☆"},
    "Espinho | Panorâmica": {"key": "bc_espinho", "forecast_key": "espinho", "source": "beachcam", "page": "https://beachcam.meo.pt/livecams/praia-de-espinho/", "stars": "★★★☆☆"},
    "Espinho HD": {"key": "espinho", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/espinho-hd", "stars": "★★★☆☆"},
    "Espinho vista aérea HD": {"key": "espinho_aerea", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/espinho-vista-aerea", "stars": "★★★☆☆"},
    "Espinho | Silvalde Beachcam": {"key": "bc_silvalde", "forecast_key": "silvalde", "source": "beachcam", "page": "https://beachcam.meo.pt/livecams/espinho-silvalde/", "stars": "★★★☆☆"},
    "Espinho - Silvalde HD": {"key": "silvalde", "page": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/espinho-silvalde", "stars": "★★★★☆"},

    "Esmoriz": {"key": "bc_esmoriz", "forecast_key": "silvalde", "source": "beachcam", "page": "https://beachcam.meo.pt/livecams/esmoriz/", "stars": "★★★☆☆"},
    "Cortegaça (Vila do Surf) HD": {"key": "cortegaca_vila", "page": "https://surftotal.com/camaras-report/aveiro/cortegaca-hd", "stars": "★★★☆☆"},
    "Furadouro": {"key": "bc_furadouro", "forecast_key": "cortegaca_vila", "source": "beachcam", "page": "https://beachcam.meo.pt/livecams/furadouro/", "stars": "★★★☆☆"},
    "Praia da Torreira": {"key": "bc_torreira", "forecast_key": "barra_norte", "source": "beachcam", "page": "https://beachcam.meo.pt/livecams/praia-da-torreira/", "stars": "★★★☆☆"},
    "Praia de São Jacinto | Barra": {"key": "bc_sao_jacinto", "forecast_key": "barra_norte", "source": "beachcam", "page": "https://beachcam.meo.pt/livecams/praia-de-sao-jacinto-barra/", "stars": "★★★☆☆"},
    "Praia da Barra Norte HD": {"key": "barra_norte", "page": "https://surftotal.com/camaras-report/aveiro/praia-da-barra-norte-hd", "stars": "★★★☆☆"},
    "Praia da Barra | Beachcam": {"key": "bc_barra", "forecast_key": "barra_norte", "source": "beachcam", "page": "https://beachcam.meo.pt/livecams/praia-da-barra/", "stars": "★★★☆☆"},
    "Costa Nova": {"key": "bc_costa_nova", "forecast_key": "barra_norte", "source": "beachcam", "page": "https://beachcam.meo.pt/livecams/costa-nova/", "stars": "★★★☆☆"},
    "Mira": {"key": "mira", "page": "https://surftotal.com/camaras-report/aveiro/mira", "stars": "★★★☆☆"},
    "Praia de Mira | Beachcam": {"key": "bc_mira", "forecast_key": "mira", "source": "beachcam", "page": "https://beachcam.meo.pt/livecams/praia-de-mira/", "stars": "★★★☆☆"},
    "Praia da Tocha": {"key": "bc_tocha", "forecast_key": "mira", "source": "beachcam", "page": "https://beachcam.meo.pt/livecams/praia-da-tocha/", "stars": "★★★☆☆"},
    "Murtinheira": {"key": "bc_murtinheira", "forecast_key": "figueira_cabedelo", "source": "beachcam", "page": "https://beachcam.meo.pt/livecams/murtinheira/", "stars": "★★★☆☆"},
    "Figueira da Foz | Buarcos": {"key": "bc_figueira_buarcos", "forecast_key": "figueira_cabedelo", "source": "beachcam", "page": "https://beachcam.meo.pt/livecams/figueira-da-foz-tamargueira/", "stars": "★★★☆☆"},
    "Figueira da Foz | Panorâmica": {"key": "bc_figueira_panoramica", "forecast_key": "figueira_cabedelo", "source": "beachcam", "page": "https://beachcam.meo.pt/livecams/figueira-da-foz-cabedelo-buarcos/", "stars": "★★★☆☆"},
    "Praia do Cabedelo (Figueira da Foz)": {"key": "figueira_cabedelo", "page": "https://surftotal.com/camaras-report/figueira-da-foz/praia-do-cabedelo-hd", "stars": "★★★☆☆"},
    "Figueira da Foz | Cabedelo Beachcam": {"key": "bc_figueira_cabedelo", "forecast_key": "figueira_cabedelo", "source": "beachcam", "page": "https://beachcam.meo.pt/livecams/figueira-da-foz-cabedelo/", "stars": "★★★☆☆"},
}

BEACHCAM_STREAMS = {
    "bc_ancora": "https://video-auth1.iol.pt/beachcam/bcvilapraiadeancora/playlist.m3u8",
    "bc_viana_cabedelo": "https://video-auth1.iol.pt/beachcam/bccabedeloviana/playlist.m3u8",
    "bc_esposende": "https://video-auth1.iol.pt/beachcam/bcesposende/playlist.m3u8",
    "bc_esposende_foz": "https://video-auth1.iol.pt/beachcam/bcfarolesposende/playlist.m3u8",
    "bc_ofir": "https://video-auth1.iol.pt/beachcam/bcofir/playlist.m3u8",
    "bc_apulia": "https://video-auth1.iol.pt/beachcam/bcapulia/playlist.m3u8",
    "bc_caxinas": "https://video-auth1.iol.pt/beachcam/bccaxinas/playlist.m3u8",
    "bc_leca_aterro": "https://video-auth1.iol.pt/beachcam/bcfarolleca/playlist.m3u8",
    "bc_leca": "https://video-auth1.iol.pt/beachcam/lecadapalmeira/playlist.m3u8",
    "bc_matosinhos": "https://video-auth1.iol.pt/beachcam/matosinhos/playlist.m3u8",
    "bc_homem_do_leme": "https://video-auth1.iol.pt/beachcam/bchomemdoleme/playlist.m3u8",
    "bc_carneiro": "https://video-auth1.iol.pt/beachcam/bccarneiro/playlist.m3u8",
    "canide": "https://video-auth1.iol.pt/beachcam/bccanidelo/playlist.m3u8",
    "bc_espinho": "https://video-auth1.iol.pt/beachcam/espinho/playlist.m3u8",
    "bc_silvalde": "https://video-auth1.iol.pt/beachcam/bcsilvade/playlist.m3u8",
    "bc_esmoriz": "https://video-auth1.iol.pt/beachcam/esmoriz/playlist.m3u8",
    "bc_furadouro": "https://video-auth1.iol.pt/beachcam/furadouro/playlist.m3u8",
    "bc_torreira": "https://video-auth1.iol.pt/beachcam/torreira/playlist.m3u8",
    "bc_sao_jacinto": "https://video-auth1.iol.pt/beachcam/bcfarolbarra/playlist.m3u8",
    "bc_barra": "https://video-auth1.iol.pt/beachcam/aveiro/playlist.m3u8",
    "bc_costa_nova": "https://video-auth1.iol.pt/beachcam/costanova/playlist.m3u8",
    "bc_mira": "https://video-auth1.iol.pt/beachcam/bcmira/playlist.m3u8",
    "bc_tocha": "https://video-auth1.iol.pt/beachcam/bctocha/playlist.m3u8",
    "bc_murtinheira": "https://video-auth1.iol.pt/beachcam/bcmurtinheira/playlist.m3u8",
    "bc_figueira_buarcos": "https://video-auth1.iol.pt/beachcam/bcfigueiradois/playlist.m3u8",
    "bc_figueira_panoramica": "https://video-auth1.iol.pt/beachcam/figueiradafoz/playlist.m3u8",
    "bc_figueira_cabedelo": "https://video-auth1.iol.pt/beachcam/bcfigueiracabeledo/playlist.m3u8",
}

for cam_data in CAMS.values():
    if cam_data.get("source") == "beachcam":
        cam_data["stream_url"] = BEACHCAM_STREAMS.get(cam_data["key"])

def source_label(data):
    return "Beachcam" if data.get("source") == "beachcam" else "Surftotal"

def data_attr(value):
    return json.dumps(value, ensure_ascii=False)

def direct_stream_status(stream_url, referer):
    try:
        res = requests.get(
            stream_url,
            headers={**HEADERS, "Referer": referer},
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        if res.status_code in (404, 410):
            return "dead"
        if res.ok and "#EXTM3U" in res.text:
            return "live"
        return "unknown"
    except Exception as e:
        print(f"ERROR checking stream: {stream_url}: {e}")
        return "unknown"

def find_m3u8(data):
    page_url = data["page"]
    fallback_stream = data.get("stream_url")
    try:
        html = requests.get(
            page_url,
            headers={**HEADERS, "Referer": page_url},
            timeout=REQUEST_TIMEOUT_SECONDS,
        ).text
        if data.get("source") == "beachcam":
            match = re.search(r'data-video-url=["\']([^"\']+?\.m3u8[^"\']*)["\']', html)
            if match:
                stream_url = match.group(1).replace("\\/", "/")
                return None if direct_stream_status(stream_url, page_url) == "dead" else stream_url
            return fallback_stream
        matches = re.findall(r'https?://[^"\']+?\.m3u8[^"\']*', html)
        return matches[0].replace("\\/", "/") if matches else None
    except Exception as e:
        print(f"ERROR finding stream: {page_url}: {e}")
        if data.get("source") == "beachcam":
            return fallback_stream
        return None

def render_cam(name, idx, data):
    forecast_key = data.get("forecast_key", data["key"])
    direct_stream = data.get("stream_url")
    direct_attr = f" data-direct-stream={data_attr(direct_stream)}" if direct_stream and data.get("source") == "beachcam" else ""
    label = source_label(data)
    return f"""
<div class="cam forecast-card" data-name={data_attr(name)} data-key={data_attr(data["key"])} data-forecast-key={data_attr(forecast_key)}{direct_attr}>
  <h2>{name}</h2>
  <video id="video{idx}" controls autoplay muted playsinline preload="none"></video>
  <div class="cam-footer">
    <button class="forecast-pill" onclick="showForecast('{forecast_key}')" title="Forecast">☆☆☆☆☆</button>
    <span class="sep">|</span>
    <button class="energy-pill" onclick="showForecast('{forecast_key}')" title="Forecast energy">-- kJ</button>
    <span class="sep">|</span>
    <span class="wind-pill">-- m/s</span>
    <span class="sep">|</span>
    <button class="refresh-icon" onclick="refreshCam('video{idx}')" title="Refresh">↻</button>
    <span class="sep">|</span>
    <a class="source-link" href="{data["page"]}" target="_blank">{label}</a>
  </div>
</div>
"""

def render_offline(name, data):
    forecast_key = data.get("forecast_key", data["key"])
    label = source_label(data)
    return f"""
<div class="offline-item forecast-card" data-name={data_attr(name)} data-key={data_attr(data["key"])} data-forecast-key={data_attr(forecast_key)}>
  <div class="offline-main">
    <span class="offline-name">{name}</span>
    <a class="source-link" href="{data["page"]}" target="_blank">{label}</a>
  </div>
  <div class="offline-stats">
    <button class="forecast-pill" onclick="showForecast('{forecast_key}')" title="Forecast">☆☆☆☆☆</button>
    <button class="energy-pill" onclick="showForecast('{forecast_key}')" title="Forecast energy">-- kJ</button>
    <span class="wind-pill">-- m/s</span>
  </div>
</div>
"""

online_names = []
offline_names = []

for name, data in CAMS.items():
    stream_url = find_m3u8(data)
    data["stream_url"] = stream_url
    if stream_url:
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
const streamRefreshes = {{}};
const forecastCache = {{}};
const TOKEN_LIFETIME_SECONDS = 300;
const TOKEN_REFRESH_BUFFER_SECONDS = 75;
const TOKEN_RETRY_SECONDS = 15;
const AUTO_REFRESH_SECONDS = 180;

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
    clearTimeout(tokenTimers[videoId]);
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
    hls.on(Hls.Events.ERROR, (event, data) => {{
      if (data.fatal) markCamFailed(videoId);
    }});
  }}
}}

function markCamFailed(videoId) {{
  const video = document.getElementById(videoId);
  const card = video?.closest(".cam");
  const el = card?.querySelector(".token-info");
  if (el) el.textContent = "⏱ failed";
  if (tokenTimers[videoId]) clearTimeout(tokenTimers[videoId]);
  tokenTimers[videoId] = setTimeout(() => startOrRefreshCam(videoId), TOKEN_RETRY_SECONDS * 1000);
}}

function updateTokenInfo(videoId, generatedAt, servedAt) {{
  const video = document.getElementById(videoId);
  const el = video?.closest(".cam")?.querySelector(".token-info");
  if (!video) return;

  function tick() {{
    const now = Math.floor(Date.now() / 1000);
    const baseAge = Math.max(0, servedAt - generatedAt);
    const age = baseAge + Math.max(0, now - servedAt);
    const left = Math.max(0, TOKEN_LIFETIME_SECONDS - age);
    if (el) el.textContent = "⏱ " + formatDuration(left);
  }}

  tick();
  if (tokenTimers[videoId]) clearTimeout(tokenTimers[videoId]);
  const expiresAt = (generatedAt + TOKEN_LIFETIME_SECONDS) * 1000;
  const refreshAt = expiresAt - TOKEN_REFRESH_BUFFER_SECONDS * 1000;
  const delay = Math.max(TOKEN_RETRY_SECONDS * 1000, refreshAt - Date.now());
  tokenTimers[videoId] = setTimeout(() => startOrRefreshCam(videoId), delay);
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
  if (streamRefreshes[videoId]) return streamRefreshes[videoId];

  const video = document.getElementById(videoId);
  const card = video?.closest(".cam");
  const camKey = card?.dataset.key;
  const directStream = card?.dataset.directStream;
  const el = card?.querySelector(".token-info");
  if (!video || !camKey) return;
  video.dataset.started = "true";

  if (directStream) {{
    initCam(videoId, directStream);
    if (el) el.textContent = "⏱ live";
    return;
  }}

  streamRefreshes[videoId] = (async () => {{
    try {{
      if (el) el.textContent = "⏱ loading";
      const data = await fetchFreshStream(camKey);
      const now = Math.floor(Date.now() / 1000);
      initCam(videoId, data.stream);
      updateTokenInfo(videoId, data.generatedAt || now, data.servedAt || now);
    }} catch (e) {{
      console.error(e);
      if (el) el.textContent = "⏱ failed";
      if (tokenTimers[videoId]) clearTimeout(tokenTimers[videoId]);
      tokenTimers[videoId] = setTimeout(() => startOrRefreshCam(videoId), TOKEN_RETRY_SECONDS * 1000);
    }} finally {{
      delete streamRefreshes[videoId];
    }}
  }})();

  return streamRefreshes[videoId];
}}

async function refreshCam(videoId) {{
  await startOrRefreshCam(videoId);
}}

async function refreshAll() {{
  const videos = Array.from(document.querySelectorAll(".cam video"));
  await Promise.allSettled(videos.map(video => startOrRefreshCam(video.id)));
}}

async function refreshStartedCams() {{
  const videos = Array.from(document.querySelectorAll('.cam video[data-started="true"]'));
  await Promise.allSettled(videos.map(video => startOrRefreshCam(video.id)));
}}

function setupLazyCams() {{
  const videos = Array.from(document.querySelectorAll(".cam video"));
  const rootMargin = window.matchMedia("(max-width: 700px)").matches
    ? "120px 0px"
    : "500px 0px";
  if (!("IntersectionObserver" in window)) {{
    videos.slice(0, window.matchMedia("(max-width: 700px)").matches ? 4 : 6)
      .forEach(video => startOrRefreshCam(video.id));
    return;
  }}

  const observer = new IntersectionObserver(entries => {{
    entries.forEach(entry => {{
      if (!entry.isIntersecting) return;
      const video = entry.target;
      observer.unobserve(video);
      startOrRefreshCam(video.id);
    }});
  }}, {{ rootMargin }});

  videos.forEach(video => observer.observe(video));
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
  const spotKey = card?.dataset.forecastKey || card?.dataset.key;
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
  const cards = Array.from(document.querySelectorAll(".forecast-card"));
  for (const card of cards) {{
    await loadForecastForCard(card);
  }}
}}

async function showForecast(spotKey) {{
  let data = forecastCache[spotKey];

  if (!data) {{
    const card = document.querySelector('.forecast-card[data-key="' + spotKey + '"]');
    await loadForecastForCard(card);
    data = forecastCache[spotKey];
  }}

  if (!data) return;

  const modal = document.getElementById("forecast-modal");
  const body = document.getElementById("forecast-modal-body");

  body.innerHTML =
    '<div class="modal-title">' + data.name + '</div>' +
    '<div class="modal-stars">' + (data.stars || "☆☆☆☆☆") + '</div>' +

    '<div class="modal-row"><b>Energy</b><span>' + (data.energyKj ?? "--") + ' kJ</span></div>' +

    '<div class="modal-row"><b>Wave</b><span>' +
      fmt(data.wave?.heightM, " m") + ' @ ' +
      fmt(data.wave?.periodS, " s") + ' ' +
      (data.wave?.directionText || "") +
    '</span></div>' +

    '<div class="modal-row"><b>Swell</b><span>' +
      fmt(data.swell?.heightM, " m") + ' @ ' +
      fmt(data.swell?.periodS, " s") + ' ' +
      (data.swell?.directionText || "") +
    '</span></div>' +

    '<div class="modal-row"><b>Wind</b><span>' +
      fmt(data.wind?.speedMs, " m/s") + ' ' +
      (data.wind?.directionText || "") +
    '</span></div>' +

    '<div class="modal-row"><b>Effect</b><span>' +
      (data.wind?.effect || "unknown") +
    '</span></div>' +

    '<div class="modal-row"><b>Tide</b><span>' +
      formatTidePhase(data.tide) +
      (data.tide?.heightM != null ? " · " + data.tide.heightM + " m" : "") +
    '</span></div>' +

    '<div class="modal-row"><b>Updated</b><span>' +
      (data.updatedLocal || "unknown") +
    '</span></div>';

  modal.classList.add("show");
}}

function closeForecastModal() {{
  document.getElementById("forecast-modal").classList.remove("show");
}}

function fmt(value, suffix) {{
  return value == null ? "--" : value + suffix;
}}

function formatTidePhase(tide) {{
  if (!tide) return "unknown";
  const reportedPhase = String(tide.phase || tide.state || "").toLowerCase().replaceAll("_", "-");
  const phase = tideDirectionFromExtremes(tide) || reportedPhase;
  const height = Number(tide.heightM);
  if (!Number.isFinite(height)) return tide.state || "unknown";
  const position = tidePosition(tide, height);

  if (phase === "rising") {{
    if (position <= 0.08) return "Low";
    if (position < 0.48) return "Low → Mid";
    if (position <= 0.52) return "Mid";
    if (position < 0.92) return "Mid → High";
    return "High";
  }}

  if (phase === "falling") {{
    if (position >= 0.92) return "High";
    if (position > 0.52) return "High → Mid";
    if (position >= 0.48) return "Mid";
    if (position > 0.08) return "Mid → Low";
    return "Low";
  }}

  return tide.state || "unknown";
}}

function tideDirectionFromExtremes(tide) {{
  const previousType = String(tide.previousExtreme?.type || "").toLowerCase();
  const nextType = String(tide.nextExtreme?.type || "").toLowerCase();
  if (previousType === "low" && nextType === "high") return "rising";
  if (previousType === "high" && nextType === "low") return "falling";
  return "";
}}

function tidePosition(tide, height) {{
  const low = firstFinite(
    extremeHeight(tide, "low"),
    tide.lowHeightM,
    tide.lowHeight,
    tide.low?.heightM,
    tide.low?.height,
    tide.previousLow?.heightM,
    tide.previousLow?.height,
    tide.range?.lowM,
    tide.range?.lowHeightM
  );
  const high = firstFinite(
    extremeHeight(tide, "high"),
    tide.highHeightM,
    tide.highHeight,
    tide.high?.heightM,
    tide.high?.height,
    tide.previousHigh?.heightM,
    tide.previousHigh?.height,
    tide.range?.highM,
    tide.range?.highHeightM
  );

  if (Number.isFinite(low) && Number.isFinite(high) && high > low) {{
    return clamp01((height - low) / (high - low));
  }}

  const suppliedPosition = Number(tide.normalizedHeight ?? tide.position);
  if (Number.isFinite(suppliedPosition)) return clamp01(suppliedPosition);

  return clamp01((height - 0.6) / (3.4 - 0.6));
}}

function extremeHeight(tide, type) {{
  const extremes = [tide.previousExtreme, tide.nextExtreme];
  const extreme = extremes.find(item =>
    String(item?.type || "").toLowerCase() === type
  );
  return Number(extreme?.heightM ?? extreme?.height);
}}

function firstFinite(...values) {{
  for (const value of values) {{
    const number = Number(value);
    if (Number.isFinite(number)) return number;
  }}
  return NaN;
}}

function clamp01(value) {{
  return Math.max(0, Math.min(1, value));
}}

window.addEventListener("load", () => {{
  setupLazyCams();
  loadAllForecasts();
  setInterval(refreshStartedCams, AUTO_REFRESH_SECONDS * 1000);
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
body {{ margin:0; font-family:ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background:#111; color:#eee; }}

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
  overflow-x:auto;
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
  overflow-x:auto;
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
.forecast-modal {{
  display:none;
  position:fixed;
  inset:0;
  background:rgba(0,0,0,0.72);
  z-index:999;
  align-items:center;
  justify-content:center;
  padding:20px;
}}

.forecast-modal.show {{
  display:flex;
}}

.forecast-modal-content {{
  position:relative;
  width:min(360px, 92vw);
  background:#1f1f1f;
  border-radius:14px;
  padding:18px;
  color:#eee;
  box-shadow:0 10px 35px rgba(0,0,0,0.5);
}}

.modal-close {{
  position:absolute;
  top:8px;
  right:10px;
  background:transparent;
  color:#aaa;
  border:0;
  font-size:24px;
  cursor:pointer;
}}

.modal-title {{
  font-size:18px;
  font-weight:bold;
  margin-bottom:6px;
}}

.modal-stars {{
  color:#ffd36a;
  font-size:20px;
  margin-bottom:14px;
}}

.modal-row {{
  display:flex;
  justify-content:space-between;
  gap:12px;
  padding:7px 0;
  border-top:1px solid #333;
  font-size:13px;
}}

.modal-row span {{
  text-align:right;
  color:#ddd;
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
  <a href="https://surftotal.com" target="_blank">Surftotal</a>
  and <a href="https://beachcam.meo.pt" target="_blank">Beachcam</a>.
</div>
<div id="forecast-modal" class="forecast-modal" onclick="closeForecastModal()">
  <div class="forecast-modal-content" onclick="event.stopPropagation()">
    <button class="modal-close" onclick="closeForecastModal()">×</button>
    <div id="forecast-modal-body"></div>
  </div>
</div>

</body>
</html>
"""

template_path = Path("index.html")
if template_path.exists():
    template = template_path.read_text(encoding="utf-8")

    def replace_generated_section(source, start_marker, end_marker, content):
        pattern = re.escape(start_marker) + r".*?" + re.escape(end_marker)
        replacement = f"{start_marker}\n{content.rstrip()}\n{end_marker}"
        updated, count = re.subn(pattern, lambda _: replacement, source, count=1, flags=re.S)
        if count != 1:
            raise RuntimeError(f"Missing generated section: {start_marker}")
        return updated

    online_html = "".join(
        render_cam(name, idx, CAMS[name])
        for idx, name in enumerate(online_names)
    )
    offline_html = "".join(
        render_offline(name, CAMS[name])
        for name in offline_names
    )
    html = replace_generated_section(
        template,
        "<!-- ONLINE_CAMS_START -->",
        "<!-- ONLINE_CAMS_END -->",
        online_html,
    )
    html = replace_generated_section(
        html,
        "<!-- OFFLINE_CAMS_START -->",
        "<!-- OFFLINE_CAMS_END -->",
        offline_html,
    )

output_path = template_path if template_path.exists() else Path("cams.html")
output_path.write_text(html, encoding="utf-8")
print(f"Generated: {output_path}")
print(f"Online: {len(online_names)}")
print(f"Offline: {len(offline_names)}")
