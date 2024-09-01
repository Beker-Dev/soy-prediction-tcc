from src.models.helpers.model_interface import ModelInterface
from src.models.helpers.model_mixin import ModelMixin

from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor


class ExtremeGradientBoostingModel(ModelInterface, ModelMixin):
    def __init__(self):
        super().__init__(model_instance=GradientBoostingRegressor())

    def train_model(self, test_size: float = 0.2, seed: int = 49) -> None:
        self.df = self._get_dataframe()
        X, y = self._get_model_train_variables()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=seed)
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        self._set_model_metrics(y_test, y_pred)
        self._set_model_variables(y_test, y_pred)
