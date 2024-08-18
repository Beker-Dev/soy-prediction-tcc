from src.dataset.nasa_power import NasaPower
from src.dataset.soy_production import SoyProduction

import json

import pandas as pd


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
                        print(f"{municipality}: union ok")
            else:
                print(f"{municipality}: not found")

        with open(output_file, "w") as outfile:
            json.dump(nasa_power_df, outfile, indent=4)

    @staticmethod
    def get_dataframe(path: str = "assets/union_dataset.json") -> pd.DataFrame:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        return pd.DataFrame(data)


DatasetUnion.unite_datasets()
