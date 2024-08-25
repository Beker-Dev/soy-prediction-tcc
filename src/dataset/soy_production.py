from src.dataset.nasa_power import NasaPower
from src.dataset.enums.soy_production import SoyProductionEnum

from typing import Any

import pandas as pd
import numpy as np
import json


class SoyProduction:
    def __init__(self, xlsx_file: str = 'assets/tabela1612_mod.xlsx', range_years: range = range(2008, 2022 + 1)):
        self.xlsx_file = xlsx_file
        self.range_years = range_years
        self.data = dict()
        self.dataframe = None

    def _set_planted_area(self) -> None:
        df = pd.read_excel(self.xlsx_file, sheet_name='Área plantada (Hectares)')

        # for some reason only this column is int
        # to avoid errors and creating unnecessary handlers
        # I've added this type casting
        df["2008"] = df[2008].astype(str)

        self._set_attr_from_dataframe(df, self.data, SoyProductionEnum.PLANTED_AREA)

    def _set_harvested_area(self) -> None:
        df = pd.read_excel(self.xlsx_file, sheet_name='Área colhida (Hectares)')
        self._set_attr_from_dataframe(df, self.data, SoyProductionEnum.HARVESTED_AREA)

    def _set_production(self) -> None:
        df = pd.read_excel(self.xlsx_file, sheet_name='Quantidade produzida (Tonela...')
        self._set_attr_from_dataframe(df, self.data, SoyProductionEnum.PRODUCTION)

    def _set_productivity(self) -> None:
        df = pd.read_excel(self.xlsx_file, sheet_name='Rendimento médio da produção...')
        df["2010"] = df[2010].astype(str)
        self._set_attr_from_dataframe(df, self.data, SoyProductionEnum.PRODUCTIVITY)

    def _set_attr_from_dataframe(self, df: Any, obj: dict, key: SoyProductionEnum) -> None:
        available_towns = NasaPower.get_dataframe().columns

        for index, row in df.iterrows():
            city = row['Município']
            city_data = {}

            if not isinstance(city, str):
                # this avoids to add a 'NaN' city
                continue

            city = city.replace(' (PR)', '')

            if city not in available_towns:
                continue

            if not obj.get(city):
                obj[city] = {}

            for year in self.range_years:
                row_value = row[str(year)]

                city_data[year] = {
                    key.name: int(row_value)
                }

            for year, c_data in city_data.items():
                if year in obj[city]:
                    obj[city][year].update(c_data)
                else:
                    obj[city][year] = c_data

    def _calculate_median(self, df_key: str) -> int:
        values = list()

        for city in self.dataframe.columns:
            for year in self.dataframe[city].keys():
                data_value = self.dataframe[city][year][df_key]
                if pd.notna(data_value) and isinstance(data_value, (int, float)):
                    values.append(data_value)

        return int(np.median(values))

    def _treat_empty_values(self, df_cell: dict) -> dict:
        possible_empty_values = [None, np.nan, 'nan', '-']
        df_keys = [e.name for e in SoyProductionEnum]

        if isinstance(df_cell, dict):
            for key in df_keys:
                df_cell[key] = (
                    self._calculate_median(key)
                    if df_cell[key] in possible_empty_values else df_cell[key]
                )

        return df_cell

    def _handle_dataset_values(self) -> None:
        self.dataframe = pd.DataFrame(data=self.data)
        self.dataframe = self.dataframe.map(self._treat_empty_values)

    def set_dataframe(self, path: str = "assets/soy_production.json") -> pd.DataFrame:
        self._set_planted_area()
        self._set_harvested_area()
        self._set_production()
        self._set_productivity()
        self._handle_dataset_values()
        self.dataframe.to_json(path, indent=4, force_ascii=False)

        return self.dataframe

    @staticmethod
    def get_dataframe(path: str = "assets/soy_production.json") -> pd.DataFrame:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        return pd.DataFrame(data)
