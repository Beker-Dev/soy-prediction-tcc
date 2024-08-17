from src.dataset.soy_production import SoyProduction
from src.dataset.eto import ETo
from src.dataset.nasa_power import NasaPower
from src.dataset.union import DatasetUnion

# -----------------------------------------------------------------------
# How to use it?
# -> Just uncomment the lines you want to run
# -> All the run lines have a brief explanation of what they do.
# -> Also all the run lines have a index, pointing their run order
#
# The complete dataset structure is organized as:
# ----- City Name
# ---------- Year
# --------------- Area
# --------------- Production
# --------------- Evapotranspiration [todo: add this field to dataframe]
# e.g: df[city][year] = {area: x, production: y, evapotranspiration: z}
#
# -----------------------------------------------------------------------

# [1] - It saves soy production data to a .json file
# soy_production = SoyProduction()
# soy_production.set_dataframe()

# [2] - It saves nasa power data to a .json file
# NasaPower.save_agrometeorological_data()

# [3] - It handles nasa power dataset, by replacing hourly data to daily data with its average and adding max, min temp
# NasaPower.clean_data()

# [4] - It gets evapotranspiration (ETo) and set them to dataframe
# todo: finish implementing this method
# eto = ETo(df)
# df = eto.include_eto_to_df()

# [5] - It joins SoyProduction and NasaPower datasets
# DatasetUnion.unite_datasets()

# [6] - It saves the complete dataset to a .json file
# todo: use the same class of index 5 to save the complete dataset in a new file to use it at ML Models
