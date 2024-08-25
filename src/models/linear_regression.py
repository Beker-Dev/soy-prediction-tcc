import random

from src.dataset.union import DatasetUnion
from src.dataset.enums.parameters import Parameters
from src.dataset.enums.soy_production import SoyProductionEnum

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import sklearn.metrics as skl_metrics
import matplotlib.pyplot as plt


class LinearRegressionModel:
    def __init__(self):
        self.model = LinearRegression()
        self.df = None
        self.mae = None
        self.mse = None
        self.rmse = None
        self.r2 = None
        self.y_test = None
        self.y_pred = None

    def plot_correlation(self):
        correlation = self.get_correlation()

        plt.figure(figsize=(11, 11))
        plt.matshow(correlation, fignum=1, cmap='coolwarm')
        plt.colorbar()
        plt.xticks(range(len(correlation.columns)), correlation.columns, rotation=45, ha='left')
        plt.yticks(range(len(correlation.columns)), correlation.columns)
        plt.title('Correlation', pad=20)
        plt.show()

    def plot_linear_regression(self):
        plt.figure(figsize=(10, 6))
        plt.scatter(self.y_test, self.y_pred, color='blue', label='Predicted vs Real')
        plt.plot(
            [self.y_test.min(), self.y_test.max()],
            [self.y_test.min(),
             self.y_test.max()],
            'r--',
            label='Optimal Fit'
        )
        plt.xlabel('Real Productivity')
        plt.ylabel('Predicted Productivity')
        plt.title('Linear Regression: Real Productivity vs Predicted Productivity')
        plt.legend()
        plt.grid(True)
        plt.show()

    def get_correlation(self):
        return self.df.corr()

    def predict(self, eto: float, planted_area: int) -> float:
        new_data = pd.DataFrame({
            Parameters.ETO.name: [eto],
            SoyProductionEnum.PLANTED_AREA.name: [planted_area]
        })
        prediction = self.model.predict(new_data)
        return round(prediction[0], 2)

    def train_model(self, seed: int = 49) -> None:
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

        self.df = pd.DataFrame(rows)

        X = self.df[[
            Parameters.ETO.name,
            SoyProductionEnum.PLANTED_AREA.name,
        ]]
        y = self.df[SoyProductionEnum.PRODUCTIVITY.name]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=seed)

        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)

        self.mae = round(skl_metrics.mean_absolute_error(y_test, y_pred), 2)
        self.mse = round(skl_metrics.mean_squared_error(y_test, y_pred), 2)
        self.rmse = round(skl_metrics.root_mean_squared_error(y_test, y_pred), 2)
        self.r2 = round(skl_metrics.r2_score(y_test, y_pred), 2)

        self.y_test = y_test
        self.y_pred = y_pred
