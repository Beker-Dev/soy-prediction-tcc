from src.dataset.soy_production import SoyProduction
from src.dataset.nasa_power import NasaPower
from src.dataset.union import DatasetUnion
from src.models.linear_regression import LinearRegressionModel


# -----------------------------------------------------------------------
# How to use it?
# -> Just uncomment the lines you want to run
# -> All the run lines have a brief explanation of what they do.
# -> Also all the run lines have an index, pointing their run order
#
# The complete dataset structure is organized as:
# ----- City Name
# ---------- Year
# --------------- Area
# --------------- Production
# --------------- Evapotranspiration
# e.g: df[city][year] = {area: x, production: y, evapotranspiration: z}
#
# -----------------------------------------------------------------------

# [1] - It saves nasa power data to a .json file
# NasaPower.save_agrometeorological_data()

# [2] - It handles nasa power dataset, by replacing hourly data to daily data with its average and adding max, min temp
# NasaPower.clean_data()

# [3] - It saves evapotranspiration data to NasaPower .json file
# NasaPower.set_eto()

# [4] - It saves soy production data to a .json file
# soy_production = SoyProduction()
# soy_production.set_dataframe()

# [5] - It joins SoyProduction and NasaPower datasets
# DatasetUnion.unite_datasets()

LinearRegressionModel.test()
