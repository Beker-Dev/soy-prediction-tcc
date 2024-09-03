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
ETO = 3.39
PLANTED_AREA = 5200

# [7] - Linear Regression Model
linear_regression_model = LinearRegressionModel()
linear_regression_model.train_model()
linear_regression_model.plot_correlation()
linear_regression_model.plot_linear_regression()
lr_predicted_productivity = linear_regression_model.predict(ETO, PLANTED_AREA)
print(
    f'{linear_regression_model.train_data}',
    f'{linear_regression_model.test_data}',
    f'productivity (kg/ha)={lr_predicted_productivity}',
    sep='\n',
    end='\n'+'-'*120+'\n'
)

# [8] - Random Forest Model
random_forest_model = RandomForestModel()
random_forest_model.train_model()
random_forest_model.plot_correlation()
rf_predicted_productivity = random_forest_model.predict(ETO, PLANTED_AREA)
print(
    f'{random_forest_model.train_data}',
    f'{random_forest_model.test_data}',
    f'productivity (kg/ha)={rf_predicted_productivity}',
    sep='\n',
    end='\n'+'-'*120+'\n'
)

# [9] - Extreme Gradient Boosting Model
extreme_gradient_boosting_model = ExtremeGradientBoostingModel()
extreme_gradient_boosting_model.train_model()
extreme_gradient_boosting_model.plot_correlation()
exb_predicted_productivity = extreme_gradient_boosting_model.predict(ETO, PLANTED_AREA)
print(
    f'{extreme_gradient_boosting_model.train_data}',
    f'{extreme_gradient_boosting_model.test_data}',
    f'productivity (kg/ha)={exb_predicted_productivity}',
    sep='\n',
    end='\n'+'-'*120+'\n'
)
