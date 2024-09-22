from src.dataset.soy_production import SoyProduction
from src.dataset.nasa_power import NasaPower
from src.dataset.union import DatasetUnion
from src.models.linear_regression import LinearRegressionModel
from src.models.random_forest import RandomForestModel
from src.models.extreme_gradient_boosting import ExtremeGradientBoostingModel

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

# model variables (use them on the models below)
model_parameters = {
    "eto": 3.39,
    "rh2m": 79.56,
    "ws2m": 0.96,
    "t2m": 22.99,
    "t2m_max": 29.57,
    "t2m_min": 18.53,
    "allsky_sfc_sw_dwn": 0.17,
    "planted_area": 5200
}
year = 2020
city = "Foz do Iguaçu"

# [7] - Linear Regression Model
linear_regression_model = LinearRegressionModel()
linear_regression_model.train_model()
print('lr', linear_regression_model.train_data)
linear_regression_model.plot_model_parameters_boxplot()
# linear_regression_model.plot_correlation()
# linear_regression_model.plot_linear_regression()
# linear_regression_model.predict(**model_parameters)
# linear_regression_model.print_model_metrics()
# linear_regression_model.plot_comparison_bars_by_year(year)
# linear_regression_model.plot_comparison_bars_by_city(city)

# [8] - Random Forest Model
random_forest_model = RandomForestModel()
random_forest_model.train_model()
print('random-forest', random_forest_model.train_data)
# random_forest_model.plot_model_parameters_boxplot()
# random_forest_model.plot_correlation()
# random_forest_model.predict(**model_parameters)
# random_forest_model.print_model_metrics()
# random_forest_model.plot_comparison_bars_by_year(year)
# random_forest_model.plot_comparison_bars_by_city(city)

# [9] - Extreme Gradient Boosting Model
extreme_gradient_boosting_model = ExtremeGradientBoostingModel()
extreme_gradient_boosting_model.train_model()
print('xgboost', extreme_gradient_boosting_model.train_data)
# extreme_gradient_boosting_model.plot_model_parameters_boxplot()
# extreme_gradient_boosting_model.plot_correlation()
# extreme_gradient_boosting_model.predict(**model_parameters)
# extreme_gradient_boosting_model.print_model_metrics()
# extreme_gradient_boosting_model.plot_comparison_bars_by_year(year)
# extreme_gradient_boosting_model.plot_comparison_bars_by_city(city)
