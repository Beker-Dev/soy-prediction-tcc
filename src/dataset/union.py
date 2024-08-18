import json
from src.dataset.nasa_power import NasaPower
from src.dataset.soy_production import SoyProduction
from pprint import pprint


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


DatasetUnion.unite_datasets()
