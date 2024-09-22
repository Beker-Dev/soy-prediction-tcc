from datetime import datetime

from src.dataset.enums.parameters import ParametersRequest, Parameters
from src.evapotranspiration.eto import ETo

import json
import time
from collections import defaultdict
from copy import deepcopy

import pandas as pd
import numpy as np
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
    def _remove_data_by_year(data: dict, years_to_remove: list[int]) -> None:
        processed_data = deepcopy(data)
        for city, years in processed_data.items():
            for year in years:
                if int(year) in years_to_remove:
                    del data[city][year]


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

        with open(save_file, "w", encoding='utf-8') as file:
            json.dump(results, file, indent=4)

    @staticmethod
    def _handle_outliers(values):
        q1 = np.percentile(values, 25)
        q3 = np.percentile(values, 75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        return [value for value in values if value < lower_bound or value > upper_bound]

    @staticmethod
    def clean_data(
            read_file: str = "assets/agromet_data_2008_2024.json",
            save_file: str = "assets/agromet_data_2008_2024_processed.json"
    ):
        with open(read_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

        processed_data = {}
        outlier_counts = {
            Parameters.T2M.name: 0,
            Parameters.RH2M.name: 0,
            Parameters.WS2M.name: 0,
            Parameters.ALLSKY_SFC_SW_DWN.name: 0
        }
        total_counts = {
            Parameters.T2M.name: 0,
            Parameters.RH2M.name: 0,
            Parameters.WS2M.name: 0,
            Parameters.ALLSKY_SFC_SW_DWN.name: 0
        }

        for city, years in data.items():
            processed_data[city] = {}
            for year, details in years.items():
                # Remove data from 2023 and 2024 to avoid inaccuracies
                if year in [2023, 2024]:
                    continue

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
                    for datetime_str, value in parameter.items():
                        date = datetime.strptime(datetime_str[:8], "%Y%m%d")

                        if date.month in {1, 9, 10, 11, 12}:
                            daily_values[date.strftime("%Y-%m-%d")].append(value)

                    processed_daily_values = {}
                    if param_name == Parameters.T2M.name:
                        processed_max_values = {}
                        processed_min_values = {}

                    for date, values in daily_values.items():
                        # -----------------------------------------------------------------
                        # Detect and treat outliers
                        outliers = NasaPower._handle_outliers(values)
                        total_counts[param_name] += len(values)
                        if outliers:
                            outlier_counts[param_name] += len(outliers)
                            median_value = round(np.median(values), 2)
                            values = [median_value if v in outliers else v for v in values]
                        # -----------------------------------------------------------------

                        avg_value = round(sum(values) / len(values), 2)
                        processed_daily_values[date] = avg_value

                        if param_name == Parameters.T2M.name:
                            max_value = round(max(values), 2)
                            min_value = round(min(values), 2)
                            processed_max_values[date] = max_value
                            processed_min_values[date] = min_value

                    processed_data[city][year]["properties"]["parameter"][param_name] = processed_daily_values
                    if param_name == Parameters.T2M.name:
                        processed_data[city][year]["properties"]["parameter"][Parameters.T2M_MAX.name] = (
                            processed_max_values
                        )
                        processed_data[city][year]["properties"]["parameter"][Parameters.T2M_MIN.name] = (
                            processed_min_values
                        )

        print('counter', outlier_counts)

        with open(save_file, 'w', encoding='utf-8') as file:
            json.dump(processed_data, file, indent=4, ensure_ascii=False)

    @staticmethod
    def set_eto(
            read_file: str = "assets/agromet_data_2008_2024_processed.json",
            save_file: str = "assets/agromet_data_2008_2024_processed_eto.json"
    ):
        with open(read_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for city, years in data.items():
            for year, details in years.items():
                processed_data = {}
                parameters = details.get("properties", {}).get("parameter", {})
                if (
                    len(parameters[Parameters.T2M.name]) ==
                    len(parameters[Parameters.T2M_MAX.name]) ==
                    len(parameters[Parameters.T2M_MIN.name]) ==
                    len(parameters[Parameters.ALLSKY_SFC_SW_DWN.name]) ==
                    len(parameters[Parameters.RH2M.name]) ==
                    len(parameters[Parameters.WS2M.name])
                ):
                    # check if all parameters have the same length to use one of them to get same date
                    for date, _ in parameters[Parameters.T2M.name].items():
                        processed_data[date] = ETo.calculate_eto(
                            latitude=data[city][year]["geometry"]["coordinates"][0],
                            altitude=int(data[city][year]["geometry"]["coordinates"][2]),
                            date=date,
                            temp_min=data[city][year]["properties"]["parameter"][Parameters.T2M_MIN.name][date],
                            temp_max=data[city][year]["properties"]["parameter"][Parameters.T2M_MAX.name][date],
                            temp_avg=data[city][year]["properties"]["parameter"][Parameters.T2M.name][date],
                            wind_speed=data[city][year]["properties"]["parameter"][Parameters.WS2M.name][date],
                            humidity=data[city][year]["properties"]["parameter"][Parameters.RH2M.name][date],
                            radiation=data[city][year]["properties"]["parameter"][Parameters.ALLSKY_SFC_SW_DWN.name][
                                date]
                        )
                    data[city][year]["properties"]["parameter"][Parameters.ETO.name] = processed_data

        with open(save_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    @staticmethod
    def get_dataframe(path: str = "assets/agromet_data_2008_2024_processed_eto.json") -> pd.DataFrame:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        return pd.DataFrame(data)
