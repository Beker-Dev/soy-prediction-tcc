from src.evapotranspiration.parameters import ParametersRequest

import json
import time
from collections import defaultdict

import pandas as pd
import requests

class NasaPower:
    def __init__(self):
        pass

    @staticmethod
    def _get_agromet_data(lat: float, lng: float, year: int, parameters: str) -> dict:
        base_url = "https://power.larc.nasa.gov/api/temporal/hourly/point"
        url = (
            f"{base_url}?parameters={parameters}&community=AG&latitude={lat}&longitude={lng}&"
            f"start={year}0101&end={year}1231&format=JSON"
        )
        response = requests.get(url)
        return response.json()

    @staticmethod
    def save_agrometeorological_data(
            read_file: str = "assets/cities_lat_long.xlsx",
            save_file: str = "assets/agromet_data_2008_2024.json"
    ) -> None:
        df = pd.read_excel(read_file)
        dados = df.set_index("Cidade").T.to_dict()

        results = {}
        parameters = ','.join([parameter.name for parameter in ParametersRequest])

        for city, coord in dados.items():
            lat = coord["Latitude"]
            lng = coord["Longitude"]
            results[city] = {}

            for year in range(2008, 2024 + 1):
                agro_data = NasaPower._get_agromet_data(lat, lng, year, parameters)
                results[city][year] = agro_data

                # Wait 1 second to avoid server overload
                time.sleep(1)

        with open(save_file, "w") as file:
            json.dump(results, file, indent=4)

    @staticmethod
    def clean_data(read_file: str = "assets/agromet_data_2008_2024.json"):
        with open(read_file, 'r') as file:
            data = json.load(file)

        processed_data = {}

        for city, years in data.items():
            processed_data[city] = {}
            for year, details in years.items():
                processed_data[city][year] = {
                    "type": details.get("type"),
                    "geometry": details.get("geometry"),
                    "properties": {
                        "parameter": {}
                    }
                }

                parameters = details.get("properties", {}).get("parameter", {})

                for param_name, parameter in parameters.items():
                    daily_values = defaultdict(list)
                    for datetime, value in parameter.items():
                        date = datetime[:8]  # "YYYYMMDD"
                        daily_values[date].append(value)

                    processed_daily_values = {}
                    for date, values in daily_values.items():
                        avg_value = round(sum(values) / len(values), 2)
                        formatted_date = f"{date[:4]}-{date[4:6]}-{date[6:]}"  # "YYYY-MM-DD"
                        processed_daily_values[formatted_date] = avg_value

                    processed_data[city][year]["properties"]["parameter"][param_name] = processed_daily_values

        with open("assets/agromet_data_2008_2024_processed.json", 'w') as file:
            json.dump(processed_data, file, indent=4)