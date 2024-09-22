from src.dataset.union import DatasetUnion
from src.dataset.enums.parameters import Parameters
from src.dataset.enums.soy_production import SoyProductionEnum

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sklearn.metrics as skl_metrics


class ModelMixin:
    def __init__(self):
        pass

    def _get_dataframe(self) -> pd.DataFrame:
        data = DatasetUnion.get_complete_dataframe().to_dict()
        parameters_key = "parameters"

        rows = []
        for city, city_data in data.items():
            for year, year_data in city_data.items():
                if year.isdigit():  # avoid year being "coordinates"
                    row = {
                        Parameters.ETO.name: year_data[parameters_key][Parameters.ETO.name],
                        Parameters.T2M.name: year_data[parameters_key][Parameters.T2M.name],
                        Parameters.T2M_MIN.name: year_data[parameters_key][Parameters.T2M_MIN.name],
                        Parameters.T2M_MAX.name: year_data[parameters_key][Parameters.T2M_MAX.name],
                        Parameters.WS2M.name: year_data[parameters_key][Parameters.WS2M.name],
                        Parameters.RH2M.name: year_data[parameters_key][Parameters.RH2M.name],
                        Parameters.ALLSKY_SFC_SW_DWN.name: year_data[parameters_key][Parameters.ALLSKY_SFC_SW_DWN.name],
                        SoyProductionEnum.HARVESTED_AREA.name: year_data[SoyProductionEnum.HARVESTED_AREA.name],
                        SoyProductionEnum.PLANTED_AREA.name: year_data[SoyProductionEnum.PLANTED_AREA.name],
                        SoyProductionEnum.PRODUCTION.name: year_data[SoyProductionEnum.PRODUCTION.name],
                        SoyProductionEnum.PRODUCTIVITY.name: year_data[SoyProductionEnum.PRODUCTIVITY.name]
                    }
                    rows.append(row)

        return pd.DataFrame(rows)

    def _set_model_metrics(self, y_train, y_train_pred, y_test, y_test_pred):
        self.train_data = {
            "mae": round(skl_metrics.mean_absolute_error(y_train, y_train_pred), 2),
            "mse": round(skl_metrics.mean_squared_error(y_train, y_train_pred), 2),
            "rmse": round(skl_metrics.root_mean_squared_error(y_train, y_train_pred), 2),
            "r2": round(skl_metrics.r2_score(y_train, y_train_pred), 2)
        }
        self.test_data = {
            "mae": round(skl_metrics.mean_absolute_error(y_test, y_test_pred), 2),
            "mse": round(skl_metrics.mean_squared_error(y_test, y_test_pred), 2),
            "rmse": round(skl_metrics.root_mean_squared_error(y_test, y_test_pred), 2),
            "r2": round(skl_metrics.r2_score(y_test, y_test_pred), 2)
        }

    def _set_model_variables(self, y_test, y_pred):
        self.y_test = y_test
        self.y_pred = y_pred

    def _get_model_train_variables(self) -> tuple:
        X = self.df[[
            Parameters.ETO.name,
            Parameters.RH2M.name,
            Parameters.WS2M.name,
            Parameters.T2M.name,
            Parameters.T2M_MAX.name,
            Parameters.T2M_MIN.name,
            Parameters.ALLSKY_SFC_SW_DWN.name,
            SoyProductionEnum.PLANTED_AREA.name,
        ]]
        y = self.df[SoyProductionEnum.PRODUCTIVITY.name]
        return X, y

    def get_correlation(self):
        return self.df.corr()

    def predict(
            self,
            eto: float,
            rh2m: float,
            ws2m: float,
            t2m: float,
            t2m_max: float,
            t2m_min: float,
            allsky_sfc_sw_dwn: float,
            planted_area: int
    ) -> float:
        new_data = pd.DataFrame({
            Parameters.ETO.name: [eto],
            Parameters.RH2M.name: [rh2m],
            Parameters.WS2M.name: [ws2m],
            Parameters.T2M.name: [t2m],
            Parameters.T2M_MAX.name: [t2m_max],
            Parameters.T2M_MIN.name: [t2m_min],
            Parameters.ALLSKY_SFC_SW_DWN.name: [allsky_sfc_sw_dwn],
            SoyProductionEnum.PLANTED_AREA.name: [planted_area]
        })
        prediction = self.model.predict(new_data)
        self.predicted_data = round(prediction[0], 2)
        return self.predicted_data

    def plot_correlation(self, plot_type='coolwarm'):
        correlation = self.get_correlation()

        plt.figure(figsize=(11, 11))
        plt.matshow(correlation, fignum=1, cmap=plot_type)
        plt.colorbar()
        plt.xticks(range(len(correlation.columns)), correlation.columns, rotation=45, ha='left')
        plt.yticks(range(len(correlation.columns)), correlation.columns)
        plt.title('Correlation', pad=20)
        plt.show()

    def print_model_metrics(self):
        print(
            f'model={self.__class__.__name__}',
            f'train_data=(rmse={self.train_data["rmse"]}, r2={self.train_data["r2"]})',
            f'test_data=(rmse={self.test_data["rmse"]}, r2={self.test_data["r2"]})',
            f'productivity (kg/ha)={self.predicted_data}',
            sep='\n',
            end='\n' + '-' * 40 + '\n'
        )

    def _get_plot_comparison_data(self) -> pd.DataFrame:
        data_dict = DatasetUnion.get_complete_dataframe().to_dict()
        records = []
        for city, years in data_dict.items():
            for year, details in years.items():
                if year.isdigit():
                    parameters = details.get('parameters')
                    model_parameters = {
                        "eto": parameters[Parameters.ETO.name],
                        "rh2m": parameters[Parameters.RH2M.name],
                        "ws2m": parameters[Parameters.WS2M.name],
                        "t2m": parameters[Parameters.T2M.name],
                        "t2m_max": parameters[Parameters.T2M_MAX.name],
                        "t2m_min": parameters[Parameters.T2M_MIN.name],
                        "allsky_sfc_sw_dwn": parameters[Parameters.ALLSKY_SFC_SW_DWN.name],
                        "planted_area": details[SoyProductionEnum.PLANTED_AREA.name]
                    }
                    record = {
                        'city': city,
                        'year': int(year),
                        'real_productivity': details[SoyProductionEnum.PRODUCTIVITY.name],
                        'predicted_productivity': self.predict(**model_parameters)
                    }
                    records.append(record)
        return pd.DataFrame(records)

    def plot_comparison_bars_by_year(self, target_year: int):
        data = self._get_plot_comparison_data()

        model_name = self.__class__.__name__
        year_data = data[data['year'] == target_year]
        cities = year_data['city'].values
        real_values = year_data['real_productivity'].values
        predicted_values = year_data['predicted_productivity'].values
        x = np.arange(len(cities))
        width = 0.35

        plt.figure(figsize=(12, 6))
        plt.bar(x - width / 2, real_values, width, label='Real Productivity', color="blue")
        plt.bar(x + width / 2, predicted_values, width, label='Predicted Productivity', color="green")

        plt.xlabel('City')
        plt.ylabel('Productivity')
        plt.title(f'Productivity comparison for year {target_year} - [{model_name}]')
        plt.xticks(x, cities, rotation=45, ha='right')
        plt.legend()
        plt.tight_layout()
        plt.show()

    def plot_comparison_bars_by_city(self, target_city: str):
        data = self._get_plot_comparison_data()

        model_name = self.__class__.__name__
        city_data = data[data['city'] == target_city]
        years = city_data['year'].values
        real_values = city_data['real_productivity'].values
        predicted_values = city_data['predicted_productivity'].values
        x = np.arange(len(years))
        width = 0.35

        plt.figure(figsize=(12, 6))
        plt.bar(x - width / 2, real_values, width, label='Real Productivity', color="blue")
        plt.bar(x + width / 2, predicted_values, width, label='Predicted Productivity', color="green")

        plt.xlabel('Year')
        plt.ylabel('Productivity')
        plt.title(f'Productivity comparison for city {target_city} - [{model_name}]')
        plt.xticks(x, years, rotation=45, ha='right')
        plt.legend()
        plt.tight_layout()
        plt.show()

    def plot_model_parameters_boxplot(self):
        data_dict = DatasetUnion.get_complete_dataframe().to_dict()

        parameters = [
            # Parameters.ETO.name,
            # Parameters.T2M_MAX.name,
            # Parameters.T2M_MIN.name,
            Parameters.T2M.name,
            Parameters.RH2M.name,
            Parameters.WS2M.name,
            Parameters.ALLSKY_SFC_SW_DWN.name,
        ]

        parameter_data = {param: [] for param in parameters}

        for city, years in data_dict.items():
            for year, details in years.items():
                if year.isdigit():
                    parameters_in_year = details.get('parameters')
                    if parameters_in_year:
                        for param in parameters:
                            if param in parameters_in_year:
                                parameter_data[param].append(parameters_in_year[param])

        for param in parameters:
            plt.figure(figsize=(8, 6))
            plt.boxplot(parameter_data[param], patch_artist=True)

            plt.xlabel('Data Points')
            plt.ylabel('Values')
            plt.title(f'Boxplot of {param}')
            plt.tight_layout()
            plt.show()
