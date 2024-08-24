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
# {
#     "parameters": dict,
#     "area": int,
#     "production": int,
# }
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

# [5] - It joins SoyProduction and NasaPower datasets and save its data to a .json file
# DatasetUnion.unite_datasets()

# [6] - It prepares united dataset to train models and save it to a .json file
# DatasetUnion.prepare_dataset_to_models()

# [7] - Linear Regression Model
# linear_regression_model = LinearRegressionModel()
# mse, r2 = linear_regression_model.train_model()
# model_correlation = linear_regression_model.get_correlation()
# predicted_production = linear_regression_model.predict(2.91, 5414)
# print(f'mse={mse} / r2={r2} / production={predicted_production}', model_correlation, sep='\n')
