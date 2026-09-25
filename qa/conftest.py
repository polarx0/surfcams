import os

import pytest
import requests


DEFAULT_BASE_URL = "https://surfcams.polarx0.workers.dev"


@pytest.fixture(scope="session")
def base_url() -> str:
    """API base URL, overridable for local/staging runs."""
    return os.getenv("SURFCAMS_BASE_URL", DEFAULT_BASE_URL).rstrip("/")


@pytest.fixture(scope="session")
def api_session() -> requests.Session:
    """Shared HTTP session with a descriptive User-Agent for live smoke tests."""
    session = requests.Session()
    session.headers.update({"User-Agent": "surfcams-qa/pytest"})
    yield session
    session.close()


@pytest.fixture(scope="session")
def api_timeout() -> float:
    return float(os.getenv("SURFCAMS_API_TIMEOUT", "15"))
