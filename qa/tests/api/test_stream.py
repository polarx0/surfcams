import pytest


@pytest.mark.parametrize("cam", ["espinho"])
def test_stream_contract_for_known_online_cameras(api_session, base_url, api_timeout, cam):
    response = api_session.get(
        f"{base_url}/stream",
        params={"cam": cam},
        timeout=api_timeout,
    )

    assert response.status_code == 200
    data = response.json()

    assert data["cam"] == cam
    assert data["pageUrl"].startswith("https://")
    assert data["stream"].startswith("https://")
    assert ".m3u8" in data["stream"]
    assert data["generatedAt"] > 0
    assert data["servedAt"] > 0


@pytest.mark.parametrize(
    "params",
    [
        {},
        {"cam": "__qa_unknown_cam__"},
    ],
)
def test_stream_rejects_missing_or_unknown_camera(api_session, base_url, api_timeout, params):
    response = api_session.get(
        f"{base_url}/stream",
        params=params,
        timeout=api_timeout,
    )

    assert response.status_code == 400
