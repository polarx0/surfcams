import re
import json
import requests
from pathlib import Path

CAMS = {
    # Minho
    "Moledo HD": "https://surftotal.com/camaras-report/minho/moledo-hd",
    "Vila Praia de Âncora HD": "https://surftotal.com/camaras-report/minho/vila-praia-de-ancora-hd",
    "Viana do Castelo HD": "https://surftotal.com/camaras-report/minho/viana-do-castelo-hd",
    "Viana Pontão HD": "https://surftotal.com/camaras-report/minho/viana-pontao-hd",
    "Ofir": "https://surftotal.com/camaras-report/minho/ofir",

    # Grande Porto
    "Aguçadoura HD": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/agucadoura-hd",
    "Póvoa de Varzim": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/povoa-de-varzim",
    "Póvoa de Varzim - Ferrari HD": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/povoa-de-varzim-ferrari-hd",
    "Azurara HD": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/azurara-hd",
    "Praia de Árvore - Areal HD": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/praia-de-arvore-areal-hd",
    "Mindelo": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/mindelo",
    "Mindelo meia laranja HD": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/mindelo-meia-laranja-hd",
    "Pedras do Corgo - Melanina HD": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/pedras-do-corgo-melanina-hd",
    "Cabo do Mundo HD": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/cabo-do-mundo-hd",
    "Leça - L'Kodak (Aterro) HD": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/leca-lkodak-aterro-hd",
    "Leça da Palmeira HD": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/leca-da-palmeira-hd",
    "Leça da Palmeira bar Oscar HD": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/leca-da-palmeira-bar-oscar-hd",
    "Matosinhos HD": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/matosinhos-hd",
    "Matosinhos - Vagas Bar HD": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/matosinhos-vagas-bar-hd",
    "Cabedelo do Porto": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/cabedelo-do-porto",
    "Espinho HD": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/espinho-hd",
    "Espinho vista aérea HD": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/espinho-vista-aerea-hd",
    "Espinho - Silvalde HD": "https://surftotal.com/camaras-report/grande-porto-douro-litoral/espinho-silvalde-hd",

    # Aveiro
    "Cortegaça (Vila do Surf) HD": "https://surftotal.com/camaras-report/aveiro/cortegaca-vila-do-surf-hd",
    "Cortegaça Onda Pontão HD": "https://surftotal.com/camaras-report/aveiro/cortegaca-onda-pontao-hd",
    "Praia da Barra Norte HD": "https://surftotal.com/camaras-report/aveiro/praia-da-barra-norte-hd",
    "Mira": "https://surftotal.com/camaras-report/aveiro/mira",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0",
}

def find_m3u8(page_url):
    html = requests.get(page_url, headers={**HEADERS, "Referer": page_url}, timeout=20).text
    matches = re.findall(r'https?://[^"\']+?\.m3u8[^"\']*', html)
    if not matches:
        return None
    return matches[0].replace("\\/", "/")

streams = {}

for name, page_url in CAMS.items():
    url = find_m3u8(page_url)
    streams[name] = {
        "page": page_url,
        "stream": url,
    }
    print(f"{name}: {url or 'NOT FOUND'}")

html = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Porto Surf Cams</title>
  <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
  <style>
    body {{
      margin: 0;
      font-family: Arial, sans-serif;
      background: #111;
      color: #eee;
    }}
    header {{
      padding: 14px 18px;
      background: #1b1b1b;
      position: sticky;
      top: 0;
      z-index: 10;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 12px;
      padding: 12px;
    }}
    .cam {{
      background: #222;
      border-radius: 10px;
      overflow: hidden;
    }}
    .cam h2 {{
      margin: 0;
      padding: 10px 12px;
      font-size: 16px;
    }}
    video {{
      width: 100%;
      height: auto;
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
  </style>
</head>
<body>
<header>
  <b>Porto Surf Cams</b>
  <span style="opacity:.7"> — generated from fresh Surftotal streams</span>
</header>

<div class="grid">
"""

for idx, (name, data) in enumerate(streams.items()):
    stream = data["stream"]
    page = data["page"]
    html += f"""
  <div class="cam">
    <h2>{name} — <a href="{page}" target="_blank">Surftotal</a></h2>
"""
    if stream:
        html += f"""
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
        }} else {{
          video.outerHTML = '<div class="bad">HLS is not supported in this browser</div>';
        }}
      }})();
    </script>
"""
    else:
        html += """
    <div class="bad">Stream URL not found. Token may be generated dynamically.</div>
"""
    html += """
  </div>
"""

html += """
</div>
</body>
</html>
"""

Path("cams.html").write_text(html, encoding="utf-8")
print("Generated: cams.html")
