import numpy as np
from sklearn.linear_model import LinearRegression


class LinearRegressionModel:
    def __init__(self):
        pass

    @staticmethod
    def run_example():
        # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html
        x = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
        # y = 1 * x_0 + 2 * x_1 + 3
        y = np.dot(x, np.array([1, 2])) + 3
        reg = LinearRegression().fit(x, y)
        reg.score(x, y)
        reg.coef_
        reg.intercept_
        print(reg.predict(np.array([[3, 5]])))
