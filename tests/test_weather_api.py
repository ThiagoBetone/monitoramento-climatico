import weather_api
import pytest


class FakeResponse:
    def raise_for_status(self):
        pass

    def json(self):
        return {
            "current": {
                "time": 1757343600,
                "temperature_2m": 25.5,
                "relative_humidity_2m": 70,
                "apparent_temperature": 26.8,
                "wind_speed_10m": 11.2,
            }
        }


def test_buscar_clima_retorna_dados_atuais(monkeypatch):
    def fake_get(url, params, timeout):
        assert url == "https://api.open-meteo.com/v1/forecast"
        assert params["latitude"] == -23.5505
        assert params["longitude"] == -46.6333
        assert params["timezone"] == "UTC"
        assert params["timeformat"] == "unixtime"
        assert timeout == 15

        return FakeResponse()

    monkeypatch.setattr(weather_api.requests, "get", fake_get)

    clima = weather_api.buscar_clima(-23.5505, -46.6333)

    assert clima["time"] == 1757343600
    assert clima["temperature_2m"] == 25.5
    assert clima["relative_humidity_2m"] == 70
    assert clima["apparent_temperature"] == 26.8
    assert clima["wind_speed_10m"] == 11.2


class FakeErrorResponse:
    def raise_for_status(self):
        raise weather_api.requests.HTTPError("Erro 500")


def test_buscar_clima_propaga_erro_http(monkeypatch):
    def fake_get(url, params, timeout):
        return FakeErrorResponse()

    monkeypatch.setattr(weather_api.requests, "get", fake_get)

    with pytest.raises(weather_api.requests.HTTPError):
        weather_api.buscar_clima(-23.5505, -46.6333)