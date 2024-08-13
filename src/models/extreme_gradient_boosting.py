from sklearn.datasets import make_regression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split


class ExtremeGradientBoostingModel:
    def __init__(self):
        pass

    @staticmethod
    def run_example():
        # https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingRegressor.html
        x, y = make_regression(random_state=0)
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, random_state=0)
        reg = GradientBoostingRegressor(random_state=0)
        reg.fit(x_train, y_train)
        reg.predict(x_test[1:2])
        print(reg.score(x_test, y_test))
