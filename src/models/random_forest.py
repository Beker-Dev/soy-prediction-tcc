from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression


class RandomForestModel:
    def __init__(self):
        pass

    @staticmethod
    def run_example():
        # https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html
        x, y = make_regression(n_features=4, n_informative=2,
                               random_state=0, shuffle=False)
        regr = RandomForestRegressor(max_depth=2, random_state=0)
        regr.fit(x, y)
        print(regr.predict([[0, 0, 0, 0]]))
