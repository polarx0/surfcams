# Norte Surf Cams

**A practical surf-camera dashboard for quickly checking real beach conditions around northern Portugal.**

Norte Surf Cams is a side project I built because deciding where to surf often meant opening several unrelated camera/provider pages, waiting for streams to load and mentally comparing conditions. I wanted one lightweight page that made that decision faster.

**Live site:** https://polarx0.github.io/surfcams/

## What it does

- Aggregates multiple surf-camera sources into one responsive dashboard.
- Plays compatible HLS streams directly in the browser.
- Tracks per-camera online/offline/disabled status.
- Lazily starts streams only when cameras are near the viewport to reduce unnecessary network and CPU usage.
- Refreshes expiring stream tokens and recovers from stale/failed playback.
- Supports favorites and filtering.
- Includes nearby-location logic while deliberately avoiding persistent storage or transmission of the user's location.
- Handles provider-specific stream-resolution behavior instead of assuming every camera works the same way.

## Why it is technically interesting

The visible page is simple, but the reliability problem is not. Different camera providers expose streams differently, some URLs expire, some require a browser/session context, and a server-side availability check does not always behave the same way as real browser playback.

The project therefore separates **provider resolution**, **publication-safe camera status**, and **client playback behavior** rather than treating every stream as a static URL.

## Architecture

```text
Camera/provider pages
        |
        v
Python resolver / site generator
        |
        +----> provider-specific availability checks
        +----> publication-safe status data
        |
        v
Generated static site
        |
        +----> GitHub Pages
        +----> browser HLS playback (hls.js)
        +----> Cloudflare Worker for runtime stream handling
```

## Reliability and QA decisions

A few design choices came directly from a QA/reliability mindset:

- A camera is not marked online merely because an old stream URL exists.
- Provider-specific checks are used where direct HLS probing is misleading.
- Public status data contains camera identity/status only; sensitive or short-lived stream URLs are not exposed in the public status file.
- Streams are stopped when off-screen and restarted/refreshed when needed.
- Page visibility, long idle periods, fullscreen playback and mobile orientation are handled explicitly.
- Generator and lifecycle behavior are covered by automated tests before publishing changes.

## Tech stack

- Python
- JavaScript / HTML / CSS
- HLS.js
- Cloudflare Workers
- GitHub Pages
- Automated validation/tests

## What this project demonstrates

Norte Surf Cams started from a personal surfing problem, but it became a useful exercise in integration testing, unreliable third-party dependencies, browser behavior, state/lifecycle handling and defensive design.

I like projects like this because they force the full cycle: identify a real problem, build a small product, observe failures in real use, diagnose them and make the system more resilient.

## Repository note

This public repository contains the generated/deployed site. The generator and provider-resolution source are maintained separately.
