import csv
from pathlib import Path

from database import list_dashboard_data


output_path = Path(__file__).resolve().parent / "weather_dashboard.csv"

with output_path.open("w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)

    writer.writerow([
        "city",
        "observed_at",
        "temperature_c",
        "apparent_temperature_c",
        "relative_humidity_pct",
        "wind_speed_kmh",
    ])

    writer.writerows(list_dashboard_data())

print(f"CSV exportado para: {output_path}")