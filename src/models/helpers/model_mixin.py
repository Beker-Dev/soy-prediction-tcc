from src.dataset.union import DatasetUnion
from src.dataset.enums.parameters import Parameters
from src.dataset.enums.soy_production import SoyProductionEnum

import matplotlib.pyplot as plt
import pandas as pd
import sklearn.metrics as skl_metrics


class ModelMixin:
    def __init__(self):
        pass

    def _get_dataframe(self) -> pd.DataFrame:
        data = DatasetUnion.get_complete_dataframe().to_dict()
        parameters_key = "parameters"

        rows = []
        for city, city_data in data.items():
            for year, year_data in city_data.items():
                if year.isdigit():  # avoid year being "coordinates"
                    row = {
                        Parameters.ETO.name: year_data[parameters_key][Parameters.ETO.name],
                        Parameters.T2M.name: year_data[parameters_key][Parameters.T2M.name],
                        Parameters.T2M_MIN.name: year_data[parameters_key][Parameters.T2M_MIN.name],
                        Parameters.T2M_MAX.name: year_data[parameters_key][Parameters.T2M_MAX.name],
                        Parameters.WS2M.name: year_data[parameters_key][Parameters.WS2M.name],
                        Parameters.RH2M.name: year_data[parameters_key][Parameters.RH2M.name],
                        Parameters.ALLSKY_SFC_SW_DWN.name: year_data[parameters_key][Parameters.ALLSKY_SFC_SW_DWN.name],
                        SoyProductionEnum.HARVESTED_AREA.name: year_data[SoyProductionEnum.HARVESTED_AREA.name],
                        SoyProductionEnum.PLANTED_AREA.name: year_data[SoyProductionEnum.PLANTED_AREA.name],
                        SoyProductionEnum.PRODUCTION.name: year_data[SoyProductionEnum.PRODUCTION.name],
                        SoyProductionEnum.PRODUCTIVITY.name: year_data[SoyProductionEnum.PRODUCTIVITY.name]
                    }
                    rows.append(row)

        return pd.DataFrame(rows)

    def _set_model_metrics(self, y_train, y_train_pred, y_test, y_test_pred):
        self.train_data = {
            "mae": round(skl_metrics.mean_absolute_error(y_train, y_train_pred), 2),
            "mse": round(skl_metrics.mean_squared_error(y_train, y_train_pred), 2),
            "rmse": round(skl_metrics.root_mean_squared_error(y_train, y_train_pred), 2),
            "r2": round(skl_metrics.r2_score(y_train, y_train_pred), 2)
        }
        self.test_data = {
            "mae": round(skl_metrics.mean_absolute_error(y_test, y_test_pred), 2),
            "mse": round(skl_metrics.mean_squared_error(y_test, y_test_pred), 2),
            "rmse": round(skl_metrics.root_mean_squared_error(y_test, y_test_pred), 2),
            "r2": round(skl_metrics.r2_score(y_test, y_test_pred), 2)
        }

    def _set_model_variables(self, y_test, y_pred):
        self.y_test = y_test
        self.y_pred = y_pred

    def _get_model_train_variables(self) -> tuple:
        X = self.df[[
            Parameters.ETO.name,
            SoyProductionEnum.PLANTED_AREA.name,
        ]]
        y = self.df[SoyProductionEnum.PRODUCTIVITY.name]
        return X, y

    def get_correlation(self):
        return self.df.corr()

    def predict(self, eto: float, planted_area: int) -> float:
        new_data = pd.DataFrame({
            Parameters.ETO.name: [eto],
            SoyProductionEnum.PLANTED_AREA.name: [planted_area]
        })
        prediction = self.model.predict(new_data)
        return round(prediction[0], 2)

    def plot_correlation(self, plot_type='coolwarm'):
        correlation = self.get_correlation()

        plt.figure(figsize=(11, 11))
        plt.matshow(correlation, fignum=1, cmap=plot_type)
        plt.colorbar()
        plt.xticks(range(len(correlation.columns)), correlation.columns, rotation=45, ha='left')
        plt.yticks(range(len(correlation.columns)), correlation.columns)
        plt.title('Correlation', pad=20)
        plt.show()

