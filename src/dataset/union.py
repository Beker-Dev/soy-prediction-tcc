from src.dataset.nasa_power import NasaPower
from src.dataset.soy_production import SoyProduction
from src.dataset.enums.soy_production import SoyProductionEnum
import json

import pandas as pd
import numpy as np


class DatasetUnion:
    def __init__(self):
        pass

    @staticmethod
    def unite_datasets(output_file="assets/union_dataset.json"):
        nasa_power_df = NasaPower.get_dataframe().to_dict()
        soy_production_df = SoyProduction.get_dataframe().to_dict()

        for municipality, yearly_data in soy_production_df.items():
            if municipality in nasa_power_df:

                for year, production_data in yearly_data.items():
                    year = str(year)

                    if year in nasa_power_df[municipality]:
                        nasa_power_df[municipality][year]["properties"]["soy_production"] = production_data

        with open(output_file, "w", encoding='utf-8') as outfile:
            json.dump(nasa_power_df, outfile, indent=4)

    @staticmethod
    def prepare_dataset_to_models(save_file: str = "assets/complete_dataset.json") -> pd.DataFrame:
        data = DatasetUnion.get_dataframe().to_dict()

        processed_data = {}

        for city, years in data.items():
            processed_data[city] = {}
            for year, details in years.items():
                processed_data[city]["coordinates"] = details["geometry"]["coordinates"]
                city_year_data = {
                    "parameters": {},
                    SoyProductionEnum.PLANTED_AREA.name: None,
                    SoyProductionEnum.HARVESTED_AREA.name: None,
                    SoyProductionEnum.PRODUCTION.name: None,
                    SoyProductionEnum.PRODUCTIVITY.name: None,
                }
                properties = details["properties"]
                parameters = properties["parameter"]
                soy_production = properties["soy_production"]

                for param_name, parameter in parameters.items():
                    year_values = []
                    for _, value in parameter.items():
                        year_values.append(value)

                    avg_value = round(sum(year_values) / len(year_values), 2)
                    city_year_data["parameters"][param_name] = avg_value

                for soy_p_name, soy_p_value in soy_production.items():
                    city_year_data[soy_p_name] = int(soy_p_value)

                processed_data[city][year] = city_year_data

        with open(save_file, 'w', encoding='utf-8') as file:
            json.dump(processed_data, file, indent=4, ensure_ascii=False)

        return pd.DataFrame(processed_data)

    @staticmethod
    def get_complete_dataframe(path: str = "assets/complete_dataset.json") -> pd.DataFrame:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        return pd.DataFrame(data)

    @staticmethod
    def get_dataframe(path: str = "assets/union_dataset.json") -> pd.DataFrame:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        return pd.DataFrame(data)
