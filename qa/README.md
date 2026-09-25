# Norte Surf Cams QA portfolio

This folder contains a small, production-facing QA suite for the live Norte Surf Cams service.
The goal is to demonstrate practical Senior QA skills on a real deployed system rather than a demo application.

## What is covered

- REST API contract checks for the forecast endpoint
- Domain sanity checks for wave, wind and tide data
- Live stream response contract checks
- Negative testing for missing and unknown inputs
- Reusable pytest fixtures for environment and HTTP session setup

The tests intentionally run against the deployed Cloudflare Worker by default. The target can be overridden with `SURFCAMS_BASE_URL` for local or staging environments.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r qa/requirements.txt
pytest qa/tests -v
```

Optional configuration:

```bash
SURFCAMS_BASE_URL=https://example-worker.dev pytest qa/tests -v
SURFCAMS_API_TIMEOUT=20 pytest qa/tests -v
```

## Why these checks

The service aggregates live camera streams plus external marine, weather and tide data. The first test layer therefore focuses on high-value integration contracts and data sanity rather than brittle exact-value assertions.

Later iterations can add Playwright browser coverage, schema validation, CI execution and failure artifacts.
