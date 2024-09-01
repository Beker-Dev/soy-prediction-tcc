from abc import ABC, abstractmethod
from typing import Union

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor


class ModelInterface(ABC):
    def __init__(
            self,
            model_instance: Union[LinearRegression, RandomForestRegressor, GradientBoostingRegressor]
    ):
        self.model = model_instance
        self.df = None
        self.mae = None
        self.mse = None
        self.rmse = None
        self.r2 = None
        self.y_test = None
        self.y_pred = None

    def train_model(self, test_size: float, seed: int):
        pass
