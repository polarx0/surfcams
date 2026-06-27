const STREAM_CACHE_TTL_SECONDS = 240;
const FORECAST_CACHE_TTL_SECONDS = 3600;
const TIDE_CACHE_TTL_SECONDS = 21600;        // 6 hours
const STATION_CACHE_TTL_SECONDS = 2592000;   // 30 days

const CAMS = {
  moledo: "https://surftotal.com/camaras-report/minho/moledo",
  ancora: "https://surftotal.com/camaras-report/minho/vila-praia-ancora",
  viana_castelo: "https://surftotal.com/camaras-report/minho/viana-do-castelo-hd",
  ofir: "https://surftotal.com/camaras-report/minho/ofir",

  agucadoura: "https://surftotal.com/camaras-report/grande-porto-douro-litoral/agucadoura",
  ferrari: "https://surftotal.com/camaras-report/grande-porto-douro-litoral/povoa-de-varzim-ferrari",
  azurara: "https://surftotal.com/camaras-report/grande-porto-douro-litoral/azurara",
  arvore: "https://surftotal.com/camaras-report/grande-porto-douro-litoral/praia-da-arvore-areal",
  mindelo: "https://surftotal.com/camaras-report/grande-porto-douro-litoral/mindelo",
  mindelo_meia_laranja: "https://surftotal.com/camaras-report/grande-porto-douro-litoral/mindelo-meia-laranja",
  pedras: "https://surftotal.com/camaras-report/grande-porto-douro-litoral/pedras-do-corgo",
  cabo: "https://surftotal.com/camaras-report/grande-porto-douro-litoral/cabo-do-mundo-hd",
  leca_aterro: "https://surftotal.com/camaras-report/grande-porto-douro-litoral/leca-kodak-aterro",
  leca: "https://surftotal.com/camaras-report/grande-porto-douro-litoral/leca-da-palmeira",
  matosinhos: "https://surftotal.com/camaras-report/grande-porto-douro-litoral/matosinhos-hd",
  vagas: "https://surftotal.com/camaras-report/grande-porto-douro-litoral/matosinhos-vagas-bar",
  cabedelo: "https://surftotal.com/camaras-report/grande-porto-douro-litoral/cabedelo-do-porto",
  espinho: "https://surftotal.com/camaras-report/grande-porto-douro-litoral/espinho-hd",
  espinho_aerea: "https://surftotal.com/camaras-report/grande-porto-douro-litoral/espinho-vista-aerea",
  silvalde: "https://surftotal.com/camaras-report/grande-porto-douro-litoral/espinho-silvalde",

  cortegaca_vila: "https://surftotal.com/camaras-report/aveiro/cortegaca-hd",
  barra_norte: "https://surftotal.com/camaras-report/aveiro/praia-da-barra-norte-hd",
  mira: "https://surftotal.com/camaras-report/aveiro/mira",
  figueira_cabedelo: "https://surftotal.com/camaras-report/figueira-da-foz/praia-do-cabedelo-hd",
};

const SPOTS = {
  moledo: { name: "Moledo", lat: 41.850, lon: -8.866, offshore: 90, tideAnchor: "north" },
  ancora: { name: "Vila Praia de Âncora", lat: 41.813, lon: -8.867, offshore: 90, tideAnchor: "north" },
  viana_castelo: { name: "Viana do Castelo", lat: 41.693, lon: -8.846, offshore: 90, tideAnchor: "north" },
  ofir: { name: "Ofir", lat: 41.512, lon: -8.784, offshore: 100, tideAnchor: "north" },

  agucadoura: { name: "Aguçadoura", lat: 41.431, lon: -8.782, offshore: 90, tideAnchor: "matosinhos" },
  ferrari: { name: "Póvoa de Varzim - Ferrari", lat: 41.384, lon: -8.774, offshore: 90, tideAnchor: "matosinhos" },
  azurara: { name: "Azurara", lat: 41.342, lon: -8.749, offshore: 90, tideAnchor: "matosinhos" },
  arvore: { name: "Praia de Árvore", lat: 41.329, lon: -8.741, offshore: 90, tideAnchor: "matosinhos" },
  mindelo: { name: "Mindelo", lat: 41.307, lon: -8.738, offshore: 90, tideAnchor: "matosinhos" },
  mindelo_meia_laranja: { name: "Mindelo Meia Laranja", lat: 41.305, lon: -8.738, offshore: 90, tideAnchor: "matosinhos" },
  pedras: { name: "Pedras do Corgo", lat: 41.270, lon: -8.728, offshore: 90, tideAnchor: "matosinhos" },
  cabo: { name: "Cabo do Mundo", lat: 41.233, lon: -8.722, offshore: 90, tideAnchor: "matosinhos" },
  leca_aterro: { name: "Leça Aterro", lat: 41.217, lon: -8.714, offshore: 90, tideAnchor: "matosinhos" },
  leca: { name: "Leça da Palmeira", lat: 41.195, lon: -8.708, offshore: 90, tideAnchor: "matosinhos" },
  matosinhos: { name: "Matosinhos", lat: 41.175, lon: -8.692, offshore: 90, tideAnchor: "matosinhos" },
  vagas: { name: "Matosinhos Vagas Bar", lat: 41.173, lon: -8.691, offshore: 90, tideAnchor: "matosinhos" },
  cabedelo: { name: "Cabedelo do Porto", lat: 41.140, lon: -8.673, offshore: 90, tideAnchor: "matosinhos" },

  espinho: { name: "Espinho", lat: 41.007, lon: -8.646, offshore: 90, tideAnchor: "espinho" },
  espinho_aerea: { name: "Espinho Vista Aérea", lat: 41.006, lon: -8.646, offshore: 90, tideAnchor: "espinho" },
  silvalde: { name: "Espinho - Silvalde", lat: 40.987, lon: -8.650, offshore: 90, tideAnchor: "espinho" },
  cortegaca_vila: { name: "Cortegaça", lat: 40.940, lon: -8.656, offshore: 90, tideAnchor: "espinho" },

  barra_norte: { name: "Praia da Barra Norte", lat: 40.642, lon: -8.748, offshore: 90, tideAnchor: "south" },
  mira: { name: "Mira", lat: 40.455, lon: -8.802, offshore: 90, tideAnchor: "south" },
  figueira_cabedelo: { name: "Praia do Cabedelo - Figueira da Foz", lat: 40.143, lon: -8.866, offshore: 90, tideAnchor: "south" },
};

const TIDE_ANCHORS = {
  north: { name: "North", lat: 41.693, lon: -8.846 },
  matosinhos: { name: "Matosinhos", lat: 41.175, lon: -8.692 },
  espinho: { name: "Espinho", lat: 41.007, lon: -8.646 },
  south: { name: "Figueira da Foz", lat: 40.143, lon: -8.866 },
};

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    if (url.pathname === "/") {
      return json({
        ok: true,
        endpoints: { stream: "/stream?cam=matosinhos", forecast: "/forecast?spot=matosinhos" },
        streamCacheTtlSeconds: STREAM_CACHE_TTL_SECONDS,
        forecastCacheTtlSeconds: FORECAST_CACHE_TTL_SECONDS,
        tideCacheTtlSeconds: TIDE_CACHE_TTL_SECONDS,
        cameras: Object.keys(CAMS),
        spots: Object.keys(SPOTS),
      });
    }

    if (url.pathname === "/forecast") return handleForecast(request, env, ctx);
    if (url.pathname === "/stream") return handleStream(request, ctx);
    return json({ error: "Not found" }, 404);
  },
};

async function handleStream(request, ctx) {
  const url = new URL(request.url);
  const cam = url.searchParams.get("cam");
  const pageUrl = CAMS[cam];
  if (!pageUrl) return json({ error: "Unknown cam", available: Object.keys(CAMS) }, 400);

  const cacheUrl = new URL(request.url);
  cacheUrl.search = `?cam=${encodeURIComponent(cam)}`;
  const cacheKey = new Request(cacheUrl.toString(), { method: "GET" });
  const cache = caches.default;
  const cached = await cache.match(cacheKey);
  if (cached) {
    try {
      const data = await cached.json();
      data.servedAt = Math.floor(Date.now() / 1000);
      return json(data);
    } catch (e) {}
  }

  const res = await fetch(pageUrl, { headers: { "User-Agent": "Mozilla/5.0", "Referer": pageUrl } });
  const html = await res.text();
  let streamUrl = null;
  const patterns = [
    /https?:\/\/stream\.surftotal\.com\/[^"'\\<\s]+index\.m3u8[^"'\\<\s]*/i,
    /https?:\\\/\\\/stream\.surftotal\.com\\\/[^"'\\<\s]+index\.m3u8[^"'\\<\s]*/i,
    /https?:\/\/[^"'\\<\s]+\.m3u8[^"'\\<\s]*/i,
    /https?:\\\/\\\/[^"'\\<\s]+\.m3u8[^"'\\<\s]*/i,
  ];
  for (const pattern of patterns) {
    const match = html.match(pattern);
    if (match) {
      streamUrl = match[0].replaceAll("\\/", "/");
      break;
    }
  }
  if (!streamUrl) {
    return json({
      error: "stream temporarily unavailable",
      cam,
      pageUrl,
      htmlLength: html.length,
      hasStreamDomain: html.includes("stream.surftotal.com"),
      hasM3u8: html.includes(".m3u8"),
    }, 404);
  }

  const now = Math.floor(Date.now() / 1000);
  const data = { cam, pageUrl, stream: streamUrl, generatedAt: now, servedAt: now };
  const responseToCache = json(data, 200, { "Cache-Control": `public, max-age=${STREAM_CACHE_TTL_SECONDS}` });
  ctx.waitUntil(cache.put(cacheKey, responseToCache.clone()));
  return json(data);
}

async function handleForecast(request, env, ctx) {
  const url = new URL(request.url);
  const spotKey = url.searchParams.get("spot");
  const spot = SPOTS[spotKey];
  if (!spot) return json({ error: "Unknown spot", usage: "/forecast?spot=matosinhos", available: Object.keys(SPOTS) }, 400);

  const cacheUrl = new URL(request.url);
  cacheUrl.search = `?spot=${encodeURIComponent(spotKey)}&v=tidecheck6`;
  const cacheKey = new Request(cacheUrl.toString(), { method: "GET" });
  const cache = caches.default;
  const cached = await cache.match(cacheKey);
  if (cached) {
    try {
      const data = await cached.json();
      const tide = await getTideForSpot(spot, env, ctx);
      const tideScore = calculateTideScore(spotKey, data.energyKj, tide.heightM);
      const rating = calculateRating({
        waveHeight: data.wave?.heightM,
        swellHeight: data.swell?.heightM,
        swellPeriod: data.swell?.periodS,
        windSpeed: data.wind?.speedMs,
        windEffect: data.wind?.effect,
        energyKj: data.energyKj,
        tideScore,
      });
      data.tide = formatTideResponse(tide, tideScore);
      data.rating = rating;
      data.stars = stars(rating);
      data.servedAt = Math.floor(Date.now() / 1000);
      return json(data);
    } catch (e) {}
  }

  const marineUrl =
    "https://marine-api.open-meteo.com/v1/marine" +
    `?latitude=${spot.lat}` +
    `&longitude=${spot.lon}` +
    "&hourly=wave_height,wave_direction,wave_period,swell_wave_height,swell_wave_direction,swell_wave_period" +
    "&timezone=Europe%2FLisbon" +
    "&forecast_days=2";

  const weatherUrl =
    "https://api.open-meteo.com/v1/forecast" +
    `?latitude=${spot.lat}` +
    `&longitude=${spot.lon}` +
    "&hourly=wind_speed_10m,wind_direction_10m" +
    "&wind_speed_unit=ms" +
    "&timezone=Europe%2FLisbon" +
    "&forecast_days=2";

  const [marineRes, weatherRes] = await Promise.all([fetch(marineUrl), fetch(weatherUrl)]);
  if (!marineRes.ok) return json({ error: "Marine forecast failed", status: marineRes.status }, 502);
  if (!weatherRes.ok) return json({ error: "Weather forecast failed", status: weatherRes.status }, 502);

  const marine = await marineRes.json();
  const weather = await weatherRes.json();
  const marineIndex = closestCurrentIndex(marine.hourly?.time);
  const weatherIndex = closestCurrentIndex(weather.hourly?.time);

  const waveHeight = valueAt(marine.hourly?.wave_height, marineIndex);
  const waveDirection = valueAt(marine.hourly?.wave_direction, marineIndex);
  const wavePeriod = valueAt(marine.hourly?.wave_period, marineIndex);
  const swellHeight = valueAt(marine.hourly?.swell_wave_height, marineIndex);
  const swellDirection = valueAt(marine.hourly?.swell_wave_direction, marineIndex);
  const swellPeriod = valueAt(marine.hourly?.swell_wave_period, marineIndex);
  const windSpeed = valueAt(weather.hourly?.wind_speed_10m, weatherIndex);
  const windDirection = valueAt(weather.hourly?.wind_direction_10m, weatherIndex);

  const energyKj = calculateSurfEnergyKj(numericOr(swellHeight, waveHeight, 0), numericOr(swellPeriod, wavePeriod, 0));
  const windEffect = calculateWindEffect(windDirection, spot.offshore);
  const tide = await getTideForSpot(spot, env, ctx);
  const tideScore = calculateTideScore(spotKey, energyKj, tide.heightM);

  const rating = calculateRating({ waveHeight, swellHeight, swellPeriod, windSpeed, windEffect, energyKj, tideScore });
  const now = Math.floor(Date.now() / 1000);

  const data = {
    spot: spotKey,
    name: spot.name,
    stars: stars(rating),
    rating,
    energyKj,
    wave: { heightM: round1(waveHeight), periodS: round1(wavePeriod), directionDeg: round0(waveDirection), directionText: compass(waveDirection) },
    swell: { heightM: round1(swellHeight), periodS: round1(swellPeriod), directionDeg: round0(swellDirection), directionText: compass(swellDirection) },
    wind: { speedMs: round1(windSpeed), directionDeg: round0(windDirection), directionText: compass(windDirection), effect: windEffect },
    tide: formatTideResponse(tide, tideScore),
    source: { marine: "Open-Meteo", weather: "Open-Meteo", tide: tide.source },
    updatedLocal: marine.hourly?.time?.[marineIndex] || null,
    generatedAt: now,
    servedAt: now,
  };

  const responseToCache = json(data, 200, { "Cache-Control": `public, max-age=${FORECAST_CACHE_TTL_SECONDS}` });
  ctx.waitUntil(cache.put(cacheKey, responseToCache.clone()));
  return json(data);
}

async function getTideForSpot(spot, env, ctx) {
  const anchorKey = spot.tideAnchor || "matosinhos";
  const anchor = TIDE_ANCHORS[anchorKey] || TIDE_ANCHORS.matosinhos;
  if (!env.TIDECHECK_API_KEY) {
    return { state: "unknown", heightM: null, datum: "unknown", source: "TideCheck missing key", station: null, anchor: anchorKey, updated: null };
  }
  try {
    const station = await getNearestTideCheckStation(anchorKey, anchor, env, ctx);
    const tide = await getTideCheckHeights(anchorKey, station, env, ctx);
    return { ...tide, source: "TideCheck", station: { id: station.id, name: station.name, label: station.label, distanceKm: station.distanceKm }, anchor: anchorKey };
  } catch (e) {
    return { state: "unknown", heightM: null, datum: "unknown", source: "TideCheck error", station: null, anchor: anchorKey, updated: null, error: e.message };
  }
}

async function getNearestTideCheckStation(anchorKey, anchor, env, ctx) {
  const cacheUrl = new URL(`https://surfcams.local/tide-station?anchor=${encodeURIComponent(anchorKey)}`);
  const cacheKey = new Request(cacheUrl.toString(), { method: "GET" });
  const cache = caches.default;
  const cached = await cache.match(cacheKey);
  if (cached) return cached.json();

  const apiUrl = "https://tidecheck.com/api/stations/nearest" + `?lat=${anchor.lat}` + `&lng=${anchor.lon}`;
  const res = await fetch(apiUrl, { headers: { "X-API-Key": env.TIDECHECK_API_KEY, "Accept": "application/json" } });
  if (!res.ok) throw new Error(`TideCheck nearest failed: ${res.status}`);
  const stations = await res.json();
  const station = Array.isArray(stations) ? stations[0] : stations;
  if (!station || !station.id) throw new Error("TideCheck station not found");

  const responseToCache = json(station, 200, { "Cache-Control": `public, max-age=${STATION_CACHE_TTL_SECONDS}` });
  ctx.waitUntil(cache.put(cacheKey, responseToCache.clone()));
  return station;
}

async function getTideCheckHeights(anchorKey, station, env, ctx) {
  const today = new Date().toISOString().slice(0, 10);
  const cacheUrl = new URL(`https://surfcams.local/tide-heights?anchor=${encodeURIComponent(anchorKey)}&station=${encodeURIComponent(station.id)}&date=${today}&v=4`);
  const cacheKey = new Request(cacheUrl.toString(), { method: "GET" });
  const cache = caches.default;
  const cached = await cache.match(cacheKey);
  if (cached) return selectCurrentTide(await cached.json());

  // Two calendar days keep the next extreme available late in the evening,
  // when the following high/low tide may already fall after midnight.
  const apiUrl = `https://tidecheck.com/api/station/${encodeURIComponent(station.id)}/tides?days=2`;
  const res = await fetch(apiUrl, { headers: { "X-API-Key": env.TIDECHECK_API_KEY, "Accept": "application/json" } });
  if (!res.ok) throw new Error(`TideCheck tides failed: ${res.status}`);
  const raw = await res.json();

  const responseToCache = json(raw, 200, { "Cache-Control": `public, max-age=${TIDE_CACHE_TTL_SECONDS}` });
  ctx.waitUntil(cache.put(cacheKey, responseToCache.clone()));
  return selectCurrentTide(raw);
}

function formatTideResponse(tide, tideScore) {
  return {
    state: tide.state,
    heightM: round2(tide.heightM),
    score: round2(tideScore),
    datum: tide.datum,
    source: tide.source,
    station: tide.station,
    anchor: tide.anchor,
    updated: tide.updated,
    previousExtreme: tide.previousExtreme,
    nextExtreme: tide.nextExtreme,
    midTideHeight: tide.midTideHeight,
  };
}

function selectCurrentTide(raw) {
  const series = raw.timeSeries || [];
  const nowMs = Date.now();
  if (!series.length) return { state: "unknown", heightM: null, datum: raw.datum || "unknown", updated: null };

  let bestIndex = 0;
  let bestDiff = Infinity;
  for (let i = 0; i < series.length; i++) {
    const diff = Math.abs(new Date(series[i].time).getTime() - nowMs);
    if (diff < bestDiff) {
      bestDiff = diff;
      bestIndex = i;
    }
  }

  const current = series[bestIndex];
  const prev = bestIndex > 0 ? series[bestIndex - 1] : null;
  const next = bestIndex < series.length - 1 ? series[bestIndex + 1] : null;
  const extremes = (raw.extremes || [])
    .filter(extreme => Number.isFinite(Number(extreme?.height)) && !Number.isNaN(new Date(extreme?.time).getTime()))
    .sort((a, b) => new Date(a.time).getTime() - new Date(b.time).getTime());
  const previousExtreme = [...extremes].reverse().find(extreme => new Date(extreme.time).getTime() <= nowMs) || null;
  const nextExtreme = extremes.find(extreme => new Date(extreme.time).getTime() > nowMs) || null;
  const normalizedPrevious = normalizeExtreme(previousExtreme);
  const normalizedNext = normalizeExtreme(nextExtreme);
  const midTideHeight = normalizedPrevious && normalizedNext
    ? round2((normalizedPrevious.height + normalizedNext.height) / 2)
    : null;

  return {
    state: calculateTideStateFromExtremes(normalizedPrevious, normalizedNext)
      || calculateTideStateFromPoints(prev, current, next),
    heightM: round2(current.height),
    datum: raw.datum || "LAT",
    updated: current.time,
    previousExtreme: normalizedPrevious,
    nextExtreme: normalizedNext,
    midTideHeight,
  };
}

function normalizeExtreme(extreme) {
  if (!extreme) return null;
  return {
    time: extreme.time,
    height: round2(Number(extreme.height)),
    type: String(extreme.type || "").toLowerCase(),
  };
}

function calculateTideStateFromExtremes(previousExtreme, nextExtreme) {
  const previousType = String(previousExtreme?.type || "").toLowerCase();
  const nextType = String(nextExtreme?.type || "").toLowerCase();
  if (previousType === "low" && nextType === "high") return "rising";
  if (previousType === "high" && nextType === "low") return "falling";
  return null;
}

function calculateTideStateFromPoints(prev, current, next) {
  if (!current || typeof current.height !== "number") return "unknown";
  if (prev && next && typeof prev.height === "number" && typeof next.height === "number") {
    if (next.height > current.height && current.height > prev.height) return "rising";
    if (next.height < current.height && current.height < prev.height) return "falling";
    if (prev.height < current.height && next.height < current.height) return "high";
    if (prev.height > current.height && next.height > current.height) return "low";
  }
  if (next && typeof next.height === "number") return next.height > current.height ? "rising" : "falling";
  if (prev && typeof prev.height === "number") return current.height > prev.height ? "rising" : "falling";
  return "stable";
}

function closestCurrentIndex(times) {
  if (!times || !times.length) return 0;
  const now = new Date();
  let bestIndex = 0;
  let bestDiff = Infinity;
  for (let i = 0; i < times.length; i++) {
    const diff = Math.abs(new Date(times[i]).getTime() - now.getTime());
    if (diff < bestDiff) {
      bestDiff = diff;
      bestIndex = i;
    }
  }
  return bestIndex;
}

function valueAt(arr, idx) { return !arr || idx == null || idx < 0 || idx >= arr.length ? null : arr[idx]; }
function numericOr(...values) { for (const value of values) if (typeof value === "number" && Number.isFinite(value)) return value; return 0; }
function calculateSurfEnergyKj(heightM, periodS) { return !heightM || !periodS ? 0 : Math.round(heightM * heightM * periodS * 20); }
function calculateWindEffect(windDeg, offshoreDeg) {
  if (typeof windDeg !== "number") return "unknown";
  const diff = angleDiff(windDeg, offshoreDeg);
  if (diff <= 45) return "offshore";
  if (diff <= 90) return "cross-offshore";
  if (diff <= 135) return "cross-onshore";
  return "onshore";
}

function calculateRating({ waveHeight, swellHeight, swellPeriod, windSpeed, windEffect, energyKj, tideScore }) {
  let score = 1;
  const h = numericOr(swellHeight, waveHeight, 0);
  const p = numericOr(swellPeriod, 0);
  const w = numericOr(windSpeed, 0);
  if (h >= 0.7) score += 0.5;
  if (h >= 1.0) score += 0.5;
  if (h >= 1.4) score += 0.5;
  if (h > 3.0) score -= 0.7;
  if (p >= 8) score += 0.5;
  if (p >= 10) score += 0.7;
  if (p >= 12) score += 0.5;
  if (energyKj >= 100) score += 0.4;
  if (energyKj >= 300) score += 0.5;
  if (energyKj >= 800) score += 0.4;
  if (energyKj > 2500) score -= 0.5;
  if (windEffect === "offshore") score += 0.8;
  if (windEffect === "cross-offshore") score += 0.4;
  if (windEffect === "cross-onshore") score -= 0.3;
  if (windEffect === "onshore") score -= 0.8;
  if (w <= 3) score += 0.4;
  else if (w <= 6) score += 0.1;
  else if (w <= 9) score -= 0.3;
  else if (w <= 12) score -= 0.7;
  else score -= 1.2;
  score += tideScore || 0;
  return Math.max(1, Math.min(5, Math.round(score)));
}

function calculateTideScore(spotKey, energyKj, tideHeightM) {
  if (typeof tideHeightM !== "number" || !Number.isFinite(tideHeightM)) return 0;
  if (spotKey === "silvalde") {
    if (energyKj < 100) return inRange(tideHeightM, 0.0, 1.5, 0.2);
    if (energyKj < 300) return inRange(tideHeightM, 0.8, 1.8, 1.2);
    if (energyKj < 500) return inRange(tideHeightM, 0.5, 1.5, 1.0);
    return inRange(tideHeightM, 0.0, 2.0, 1.2);
  }
  if (spotKey === "espinho" || spotKey === "espinho_aerea") {
    if (energyKj < 200) return -0.8;
    if (energyKj < 300) return inRange(tideHeightM, 0.0, 1.0, 0.0);
    if (energyKj < 500) return inRange(tideHeightM, 0.0, 1.5, 0.0);
    if (energyKj >= 800) return inRange(tideHeightM, 0.0, 2.5, 0.7);
    return inRange(tideHeightM, 0.0, 1.5, 0.0);
  }
  return 0;
}

function inRange(value, min, max, ideal) {
  if (value < min || value > max) return -0.5;
  const left = Math.max(0.1, ideal - min);
  const right = Math.max(0.1, max - ideal);
  const width = value <= ideal ? left : right;
  const distance = Math.abs(value - ideal);
  return Math.max(0, 0.6 - (distance / width) * 0.6);
}

function stars(rating) { return "★★★★★".slice(0, rating) + "☆☆☆☆☆".slice(0, 5 - rating); }
function angleDiff(a, b) { return Math.abs((((a - b) % 360) + 540) % 360 - 180); }
function compass(deg) { if (typeof deg !== "number") return "unknown"; const dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]; return dirs[Math.round(deg / 45) % 8]; }
function round0(v) { return typeof v === "number" && Number.isFinite(v) ? Math.round(v) : null; }
function round1(v) { return typeof v === "number" && Number.isFinite(v) ? Math.round(v * 10) / 10 : null; }
function round2(v) { return typeof v === "number" && Number.isFinite(v) ? Math.round(v * 100) / 100 : null; }

function json(data, status = 200, extraHeaders = {}) {
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*", "Cache-Control": "no-store", ...extraHeaders },
  });
}
