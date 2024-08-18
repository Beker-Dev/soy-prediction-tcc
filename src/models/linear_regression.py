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

    @staticmethod
    def test():
        data = DatasetUnion.get_dataframe().to_dict()

        cities = []
        _years = []
        evapotranspirations = []
        productions = []
        areas = []

        for city, years in data.items():
            for year, details in years.items():
                cities.append(city)
                _years.append(year)
                properties = details.get("properties")
                for p_name, p_values in properties.items():
                    for key, value in p_values.items():
                        if key == 'area':
                            areas.append(value)
                        if key == 'production':
                            productions.append(value)
                        if key == Parameters.ETO.name:
                            evapotranspirations.append(random.uniform(1.5, 4))
                            # evapotranspirations.append(property['parameter'][Parameters.ETO.name])
                        # print(city, year, p_name, key, len(areas), len(productions), len(evapotranspirations))
                        # input('?')

        print(
            len(cities),
            len(_years),
            len(evapotranspirations),
            len(productions),
            len(areas)
        )

        # Criando um DataFrame
        data = pd.DataFrame({
            'Evapotranspiração': evapotranspirations,
            'Produtividade': productions
        })

        # Calculando a correlação
        correlacao = data.corr().loc['Evapotranspiração', 'Produtividade']
        print(f"Correlação entre Evapotranspiração e Produtividade: {correlacao:.2f}")

        df = pd.DataFrame({
            'city': cities,
            'year': _years,
            'area': areas,
            'evapotranspiration': evapotranspirations,
            'production': productions
        })

        model = LinearRegression()

        X = df[['area', 'evapotranspiration']]
        y = df['production']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        print(f"Mean Squared Error: {mse}")
        print(f"R^2 Score: {r2}")

        #----------------------------------------------------
        new_data = {'area': 18010, 'evapotranspiration': 0.35} # 36546
        input_df = pd.DataFrame([new_data])
        predicted_production = model.predict(input_df)
        print(
            f"Previsão de produção para área {new_data['area']} e evapotranspiração {new_data['evapotranspiration']}: {predicted_production[0]}"
        )

