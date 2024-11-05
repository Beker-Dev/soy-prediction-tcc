from src.models.helpers.model_interface import ModelInterface
from src.models.helpers.model_mixin import ModelMixin

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import pandas as pd


class RandomForestModel(ModelInterface, ModelMixin):
    def __init__(self):
        super().__init__(model_instance=RandomForestRegressor())

    def train_model(self, test_size: float = 0.2, seed: int = 49) -> None:
        self.model.random_state = seed
        self.df = self._get_dataframe()
        X, y = self._get_model_train_variables()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=seed)
        self.model.fit(X_train, y_train)
        y_train_pred = self.model.predict(X_train)
        y_test_pred = self.model.predict(X_test)
        self._set_model_metrics(y_train, y_train_pred, y_test, y_test_pred)
        self._set_model_variables(y_test, y_test_pred)

    def get_feature_importances(self):
        feature_importances = self.model.feature_importances_
        X = self._get_model_train_variables()[0]
        feature_names = X.columns
        feature_importances_df = pd.DataFrame({
            "feature": feature_names,
            "importance": feature_importances
        })
        feature_importance_df = feature_importances_df.sort_values(by='importance', ascending=False)
        return feature_importance_df

    def plot_feature_importances(self, as_graph=True):
        feature_importances_df = self.get_feature_importances()

        if as_graph:
            plt.figure(figsize=(10, 6))
            plt.barh(feature_importances_df['feature'], feature_importances_df['importance'])
            plt.xlabel("Feature Importance")
            plt.ylabel("Feature")
            plt.title("Feature Importances - Random Forest")
            plt.gca().invert_yaxis()
            plt.show()
        else:
            print(feature_importances_df)
