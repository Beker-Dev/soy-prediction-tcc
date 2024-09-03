from src.models.helpers.model_interface import ModelInterface
from src.models.helpers.model_mixin import ModelMixin

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


class LinearRegressionModel(ModelInterface, ModelMixin):
    def __init__(self):
        super().__init__(model_instance=LinearRegression())

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

    def train_model(self, test_size: float = 0.2, seed: int = 49) -> None:
        self.df = self._get_dataframe()
        X, y = self._get_model_train_variables()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=seed)
        self.model.fit(X_train, y_train)
        y_train_pred = self.model.predict(X_train)
        y_test_pred = self.model.predict(X_test)
        self._set_model_metrics(y_train, y_train_pred, y_test, y_test_pred)
        self._set_model_variables(y_test, y_test_pred)
