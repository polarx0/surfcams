import pytest


@pytest.mark.parametrize("spot", ["espinho", "matosinhos", "ofir"])
def test_forecast_contract_for_known_spots(api_session, base_url, api_timeout, spot):
    response = api_session.get(
        f"{base_url}/forecast",
        params={"spot": spot},
        timeout=api_timeout,
    )

    assert response.status_code == 200
    data = response.json()

    assert data["spot"] == spot
    assert isinstance(data["name"], str) and data["name"]

    rating = data["rating"]
    assert isinstance(rating, (int, float))
    assert 0 <= rating <= 5

    wave = data["wave"]
    assert wave["heightM"] >= 0
    assert wave["periodS"] > 0
    assert 0 <= wave["directionDeg"] < 360
    assert isinstance(wave["directionText"], str) and wave["directionText"]

    wind = data["wind"]
    assert wind["speedMs"] >= 0
    assert 0 <= wind["directionDeg"] < 360
    assert isinstance(wind["directionText"], str) and wind["directionText"]

    assert data["source"]["marine"]
    assert data["source"]["weather"]
    assert data["generatedAt"] > 0
    assert data["servedAt"] > 0


def test_forecast_tide_contract(api_session, base_url, api_timeout):
    response = api_session.get(
        f"{base_url}/forecast",
        params={"spot": "espinho"},
        timeout=api_timeout,
    )

    assert response.status_code == 200
    tide = response.json()["tide"]

    assert tide["state"] in {"rising", "falling", "high", "low"}
    assert isinstance(tide["heightM"], (int, float))
    assert tide["datum"]
    assert tide["source"]

    previous = tide["previousExtreme"]
    following = tide["nextExtreme"]
    assert previous["type"] in {"low", "high"}
    assert following["type"] in {"low", "high"}
    assert previous["type"] != following["type"]
    assert previous["time"] < following["time"]


@pytest.mark.parametrize(
    "params",
    [
        {},
        {"spot": "__qa_unknown_spot__"},
    ],
)
def test_forecast_rejects_missing_or_unknown_spot(api_session, base_url, api_timeout, params):
    response = api_session.get(
        f"{base_url}/forecast",
        params=params,
        timeout=api_timeout,
    )

    assert response.status_code == 400
