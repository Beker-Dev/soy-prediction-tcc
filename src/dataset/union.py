from src.dataset.nasa_power import NasaPower
from src.dataset.soy_production import SoyProduction


class DatasetUnion:
    def __init__(self):
        pass

    @staticmethod
    def unite_datasets():
        nasa_power_df = NasaPower.get_dataframe()
        soy_production_df = SoyProduction.get_dataframe()
