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
        self.train_data = None
        self.test_data = None
        self.y_test = None
        self.y_pred = None
        self.predicted_data = None

    @abstractmethod
    def train_model(self, test_size: float, seed: int):
        pass
