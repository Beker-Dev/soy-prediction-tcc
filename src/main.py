from src.dataset.soy_production import SoyProductionDataset
from src.dataset.eto import ETo
from src.dataset.nasa_power import NasaPower


# # Gets soy production dataframe
# soy_production_dataset = SoyProductionDataset()
# df = soy_production_dataset.get_dataframe()
#
# # Gets evapotranspiration (ETo) and set them to dataframe
# eto = ETo(df)
# df = eto.include_eto_to_df()

NasaPower.save_agrometeorological_data()
