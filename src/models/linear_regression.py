import random

from src.dataset.union import DatasetUnion
from src.dataset.enums.parameters import Parameters
from src.dataset.enums.soy_production import SoyProductionEnum

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, root_mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt


class LinearRegressionModel:
    def __init__(self):
        self.model = LinearRegression()
        self.df = None
        self.mae = None
        self.mse = None
        self.rmse = None
        self.r2 = None

    def plot_correlation(self):
        correlation = self.get_correlation()

        plt.figure(figsize=(11, 11))
        plt.matshow(correlation, fignum=1, cmap='coolwarm')
        plt.colorbar()
        plt.xticks(range(len(correlation.columns)), correlation.columns, rotation=45, ha='left')
        plt.yticks(range(len(correlation.columns)), correlation.columns)
        plt.title('Correlation Matrix', pad=20)
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

        self.mae = round(mean_absolute_error(y_test, y_pred), 2)
        self.mse = round(mean_squared_error(y_test, y_pred), 2)
        self.rmse = round(root_mean_squared_error(y_test, y_pred), 2)
        self.r2 = round(r2_score(y_test, y_pred), 2)
