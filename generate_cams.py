import re
import json
import time
import requests
import urllib.parse
from pathlib import Path
from datetime import datetime

HEADERS = {"User-Agent": "Mozilla/5.0"}
GITHUB_WORKFLOW_URL = "https://github.com/polarx0/surfcams/actions/workflows/update.yml"

CAMS = {
    "Aguçadoura HD": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/agucadoura-hd",
    "Póvoa de Varzim - Ferrari HD": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/povoa-de-varzim-ferrari",
    "Azurara HD": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/azurara-hd",
    "Praia de Árvore - Areal HD": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/praia-da-arvore-areal",
    "Mindelo": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/mindelo",
    "Mindelo meia laranja HD": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/mindelo-meia-laranja-hd",
    "Pedras do Corgo - Melanina HD": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/pedras-do-corgo",
    "Cabo do Mundo HD": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/cabo-do-mundo",
    "Leça - L'Kodak (Aterro) HD": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/leca-lkodak-aterro",
    "Leça da Palmeira HD": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/leca-da-palmeira",
    "Matosinhos HD": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/matosinhos-hd",
    "Matosinhos - Vagas Bar HD": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/matosinhos-vagas-bar",
    "Cabedelo do Porto": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/cabedelo-do-porto",
    "Espinho HD": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/espinho-hd",
    "Espinho vista aérea HD": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/espinho-vista-aerea",
    "Espinho - Silvalde HD": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/espinho-silvalde",
}

def now_human():
    return datetime.now().strftime("%H:%M:%S")

def fmt_ts(ts):
    if not ts:
        return "unknown"
    return datetime.fromtimestamp(ts).strftime("%H:%M:%S")

def find_m3u8(page_url):
    try:
        html = requests.get(page_url, headers={**HEADERS, "Referer": page_url}, timeout=20).text
        matches = re.findall(r'https?://[^"\']+?\.m3u8[^"\']*', html)
        return matches[0].replace("\\/", "/") if matches else None
    except Exception as e:
        print(f"ERROR finding stream: {page_url}: {e}")
        return None

def stream_time_ts(stream_url):
    if not stream_url:
        return None
    try:
        params = urllib.parse.parse_qs(urllib.parse.urlparse(stream_url).query)
        return int(params["time"][0]) if "time" in params else None
    except Exception:
        return None

def render_cam(name, idx, data):
    return f"""
<div class="cam" data-name="{name}">
  <h2>{name}</h2>
  <video id="video{idx}" controls autoplay muted playsinline></video>
  <div class="cam-footer">
    <span>stream time: {fmt_ts(data["stream_time"])}</span>
    <button onclick="refreshCam({json.dumps(name)}, 'video{idx}')">Refresh</button>
    <a href="{data["page"]}" target="_blank">Surftotal</a>
  </div>
  <script>
    initCam("video{idx}", {json.dumps(data["stream"])});
  </script>
</div>
"""

streams = {}
generated_at = int(time.time())
generated_at_human = now_human()

for name, page_url in CAMS.items():
    stream_url = find_m3u8(page_url)
    stime = stream_time_ts(stream_url)

    streams[name] = {
        "name": name,
        "page": page_url,
        "stream": stream_url,
        "online": stream_url is not None,
        "stream_time": stime,
        "stream_time_human": fmt_ts(stime),
    }

    print(f"{name}: {'ONLINE' if stream_url else 'OFFLINE'} stream_time={fmt_ts(stime)}")

online_names = [n for n, d in streams.items() if d["online"]]
offline_names = [n for n, d in streams.items() if not d["online"]]

Path("streams.json").write_text(
    json.dumps(
        {
            "generated_at": generated_at,
            "generated_at_human": generated_at_human,
            "streams": streams,
        },
        ensure_ascii=False,
        indent=2,
    ),
    encoding="utf-8",
)

js = """
<script>
const hlsInstances = {};

function initCam(videoId, src) {
  const video = document.getElementById(videoId);
  if (!src || !video) return;

  if (hlsInstances[videoId]) {
    hlsInstances[videoId].destroy();
    delete hlsInstances[videoId];
  }

  video.pause();
  video.removeAttribute("src");
  video.load();

  if (video.canPlayType("application/vnd.apple.mpegurl")) {
    video.src = src;
    video.play().catch(() => {});
  } else if (Hls.isSupported()) {
    const hls = new Hls();
    hlsInstances[videoId] = hls;
    hls.loadSource(src);
    hls.attachMedia(video);
    hls.on(Hls.Events.MANIFEST_PARSED, function() {
      video.play().catch(() => {});
    });
  }
}

async function refreshCam(name, videoId) {
  try {
    const response = await fetch("streams.json?t=" + Date.now(), { cache: "no-store" });
    const data = await response.json();
    const cam = data.streams[name];

    if (!cam || !cam.stream) {
      alert("No fresh stream for " + name);
      return;
    }

    initCam(videoId, cam.stream);

    const card = document.querySelector('[data-name="' + CSS.escape(name) + '"]');
    if (card) {
      const footer = card.querySelector(".cam-footer span");
      if (footer) footer.textContent = "stream time: " + (cam.stream_time_human || "unknown");
    }
  } catch (e) {
    alert("Refresh failed. Use full page refresh or Regenerate.");
  }
}

function toggleBlock(id, button, showText, hideText) {
  const block = document.getElementById(id);
  if (block.style.display === "none" || block.style.display === "") {
    block.style.display = "block";
    button.textContent = hideText;
  } else {
    block.style.display = "none";
    button.textContent = showText;
  }
}
</script>
"""

html = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Grande Porto Surf Cams</title>
<script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
{js}
<style>
body {{ margin:0; font-family:Arial,sans-serif; background:#111; color:#eee; }}
header {{ padding:10px 12px; background:#1b1b1b; position:sticky; top:0; z-index:10; }}
button {{ margin:4px; padding:7px 10px; cursor:pointer; border-radius:6px; border:0; }}
.grid {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:8px; padding:8px; }}
.cam {{ background:#222; border-radius:10px; overflow:hidden; }}
.cam h2 {{ margin:0; padding:8px 10px; font-size:14px; line-height:1.2; }}
video {{ width:100%; background:#000; display:block; }}
.cam-footer {{ display:flex; gap:8px; align-items:center; flex-wrap:wrap; padding:7px 10px 9px; font-size:12px; }}
a {{ color:#8ecbff; }}
.bad {{ padding:12px; color:#ffb3b3; }}
#offlineCams {{ display:none; }}
.offline-list {{ padding:0 12px 20px; }}
.offline-item {{ padding:8px 10px; background:#222; margin-bottom:6px; border-radius:8px; }}
@media (max-width:600px) {{
  .grid {{ grid-template-columns:repeat(2,minmax(0,1fr)); gap:6px; padding:6px; }}
  .cam h2 {{ font-size:11px; padding:6px 7px; }}
  .cam-footer {{ font-size:10px; padding:6px 7px 8px; gap:4px; }}
  button {{ font-size:11px; padding:5px 7px; }}
}}
</style>
</head>
<body>

<header>
  <b>Grande Porto Surf Cams</b><br>
  <span>streams generated: {generated_at_human}</span><br>
  <button onclick="window.location.reload()">Refresh Page</button>
  <button onclick="window.open('{GITHUB_WORKFLOW_URL}', '_blank')">Regenerate</button>
  <button onclick="toggleBlock('offlineCams', this, 'Show Offline', 'Hide Offline')">Show Offline</button>
</header>

<h2 style="padding-left:12px">🌊 Online Cameras</h2>
"""

if online_names:
    html += '<div class="grid">\n'
    for idx, name in enumerate(online_names):
        html += render_cam(name, idx, streams[name])
    html += "</div>\n"
else:
    html += '<div class="bad">No cameras are currently online.</div>\n'

html += """
<div id="offlineCams">
<h2 style="padding-left:12px">⚠️ Offline / unavailable</h2>
<div class="offline-list">
"""

for name in offline_names:
    html += f'<div class="offline-item"><a href="{streams[name]["page"]}" target="_blank">{name}</a></div>\n'

html += """
</div>
</div>

</body>
</html>
"""

Path("cams.html").write_text(html, encoding="utf-8")

print("Generated: cams.html")
print("Generated: streams.json")
print(f"Online: {len(online_names)}")
print(f"Offline: {len(offline_names)}")
print(f"Streams generated: {generated_at_human}")
