import requests


def buscar_clima(latitude, longitude):
    resposta = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": (
                "temperature_2m,relative_humidity_2m,"
                "apparent_temperature,wind_speed_10m"
            ),
            "timezone": "UTC",
            "timeformat": "unixtime",
        },
        timeout=15,
    )

    resposta.raise_for_status()
    return resposta.json()["current"]