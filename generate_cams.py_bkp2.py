import re
import json
import requests
from pathlib import Path
import urllib.parse

if stream_url and "time=" in stream_url:
    parsed = urllib.parse.urlparse(stream_url)
    params = urllib.parse.parse_qs(parsed.query)

    if "time" in params:
        print(name, params["time"][0])
HEADERS = {
    "User-Agent": "Mozilla/5.0",
}

GITHUB_WORKFLOW_URL = "https://github.com/polarx0/surfcams/actions/workflows/update.yml"

CAMS = {
    "Aguçadoura HD": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/agucadoura",
    "Póvoa de Varzim": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/povoa-de-varzim",
    "Póvoa de Varzim - Ferrari HD": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/povoa-de-varzim-ferrari",
    "Azurara HD": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/azurara",
    "Praia de Árvore - Areal HD": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/praia-da-arvore-areal",
    "Mindelo": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/mindelo",
    "Mindelo meia laranja HD": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/mindelo-meia-laranja",
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

def find_m3u8(page_url):
    try:
        html = requests.get(
            page_url,
            headers={**HEADERS, "Referer": page_url},
            timeout=20,
        ).text

        matches = re.findall(r'https?://[^"\']+?\.m3u8[^"\']*', html)
        if not matches:
            return None

        return matches[0].replace("\\/", "/")
    except Exception as e:
        print(f"ERROR finding stream: {page_url}: {e}")
        return None

def is_stream_alive(stream_url, referer):
    if not stream_url:
        return False

    try:
        r = requests.get(
            stream_url,
            headers={**HEADERS, "Referer": referer},
            timeout=10,
            allow_redirects=True,
        )
        return r.status_code == 200 and "#EXTM3U" in r.text[:300]
    except Exception:
        return False

def render_cam(name, idx, data):
    stream = data["stream"]
    page = data["page"]

    return f"""
<div class="cam">
  <h2>{name} — <a href="{page}" target="_blank">Surftotal</a></h2>
  <video id="video{idx}" controls autoplay muted playsinline></video>
  <script>
    (function() {{
      const video = document.getElementById("video{idx}");
      const src = {json.dumps(stream)};

      if (video.canPlayType("application/vnd.apple.mpegurl")) {{
        video.src = src;
      }} else if (Hls.isSupported()) {{
        const hls = new Hls();
        hls.loadSource(src);
        hls.attachMedia(video);
        hls.on(Hls.Events.MANIFEST_PARSED, function() {{
          video.play().catch(() => {{}});
        }});
      }}

      video.play().catch(() => {{}});
    }})();
  </script>
</div>
"""

def render_offline(name, data):
    page = data["page"]
    return f"""
<div class="offline-item">
  <a href="{page}" target="_blank">{name}</a>
</div>
"""

streams = {}

for name, page_url in CAMS.items():
    stream_url = find_m3u8(page_url)
    alive = is_stream_alive(stream_url, page_url)

    streams[name] = {
        "page": page_url,
        "stream": stream_url,
        "alive": alive,
    }

    print(f"{name}: {'OK' if alive else 'OFFLINE'}")

working_names = [name for name, data in streams.items() if data["alive"]]
offline_names = [name for name, data in streams.items() if not data["alive"]]

html = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Grande Porto Surf Cams</title>
<script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
<style>
body {{
  margin: 0;
  font-family: Arial, sans-serif;
  background: #111;
  color: #eee;
}}

header {{
  padding: 10px 12px;
  background: #1b1b1b;
  position: sticky;
  top: 0;
  z-index: 10;
}}

header b {{
  display: inline-block;
  margin-right: 8px;
}}

button {{
  margin: 4px 4px 4px 0;
  padding: 7px 10px;
  cursor: pointer;
  border-radius: 6px;
  border: 0;
}}

.grid {{
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px;
  padding: 8px;
}}

.cam {{
  background: #222;
  border-radius: 10px;
  overflow: hidden;
}}

.cam h2 {{
  margin: 0;
  padding: 8px 10px;
  font-size: 14px;
  line-height: 1.2;
}}

video {{
  width: 100%;
  background: #000;
  display: block;
}}

.bad {{
  padding: 12px;
  color: #ffb3b3;
}}

a {{
  color: #8ecbff;
}}

#offlineCams {{
  display: none;
}}

.offline-list {{
  padding: 0 12px 20px;
}}

.offline-item {{
  padding: 8px 10px;
  background: #222;
  margin-bottom: 6px;
  border-radius: 8px;
}}

@media (max-width: 600px) {{
  header {{
    padding: 8px;
  }}

  .grid {{
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 6px;
    padding: 6px;
  }}

  .cam h2 {{
    font-size: 11px;
    padding: 6px 7px;
  }}

  button {{
    font-size: 12px;
    padding: 6px 8px;
  }}
}}
</style>
</head>
<body>

<header>
  <b>Grande Porto Surf Cams</b>
  <button onclick="window.location.reload()">Refresh Page</button>
  <button onclick="window.open('{GITHUB_WORKFLOW_URL}', '_blank')">Regenerate</button>
  <button onclick="toggleBlock('offlineCams', this, 'Show Offline Cameras', 'Hide Offline Cameras')">Show Offline Cameras</button>
</header>

<h2 style="padding-left:12px">🌊 Online Cameras</h2>
"""

idx = 0

if working_names:
    html += """
<div class="grid">
"""
    for name in working_names:
        html += render_cam(name, idx, streams[name])
        idx += 1

    html += """
</div>
"""
else:
    html += """
<div class="bad">No Grande Porto cameras are currently online.</div>
"""

html += """
<div id="offlineCams">
<h2 style="padding-left:12px">⚠️ Offline / unavailable</h2>
<div class="offline-list">
"""

for name in offline_names:
    html += render_offline(name, streams[name])

html += """
</div>
</div>

<script>
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

</body>
</html>
"""

Path("cams.html").write_text(html, encoding="utf-8")

print("Generated: cams.html")
print(f"Online: {len(working_names)}")
print(f"Offline: {len(offline_names)}")
