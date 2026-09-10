import requests

from weather_api import buscar_clima
from database import initialize_db
from weather_service import collect_and_store_weather

def main():
    initialize_db()

    try:
        observation_id = collect_and_store_weather(
            "Assis",
            -22.6619,
            -50.4119,
        )

        print(f"Observação salva com ID: {observation_id}")

    except requests.RequestException as erro:
        print(f"Erro ao consultar o clima: {erro}")


if __name__ == "__main__":
    main()