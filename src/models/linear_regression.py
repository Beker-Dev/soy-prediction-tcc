import random

from src.dataset.union import DatasetUnion
from src.evapotranspiration.parameters import Parameters

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score


class LinearRegressionModel:
    def __init__(self):
        self.model = LinearRegression()
        self.df = None

    def get_correlation(self):
        return self.df.corr()

    def predict(self, eto: float, area: int) -> float:
        new_data = pd.DataFrame({"ETO": [eto], "area": [area]})
        prediction = self.model.predict(new_data)
        return round(prediction[0], 2)

    def train_model(self) -> tuple[float, float]:
        data = DatasetUnion.get_complete_dataframe().to_dict()

        rows = []
        for city, city_data in data.items():
            for year, year_data in city_data.items():
                if year.isdigit():  # avoid year being "coordinates"
                    row = {
                        "ETO": year_data["parameters"]["ETO"],
                        "area": year_data["area"],
                        "production": year_data["production"]
                    }
                    rows.append(row)

        self.df = pd.DataFrame(rows)

        X = self.df[["ETO", "area"]]
        y = self.df["production"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)

        mse = round(mean_squared_error(y_test, y_pred), 2)
        r2 = round(r2_score(y_test, y_pred), 2)
        return mse, r2
