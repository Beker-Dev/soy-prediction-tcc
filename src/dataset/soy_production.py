from typing import Any

import pandas as pd
import numpy as np
import json


class SoyProductionDataset:
    def __init__(self, xlsx_file: str = 'assets/tabela1612_mod.xlsx', range_years: range = range(2008, 2022 + 1)):
        self.xlsx_file = xlsx_file
        self.range_years = range_years
        self.data = dict()
        self.dataframe = None

    def _set_area(self) -> None:
        area_df = pd.read_excel(self.xlsx_file, sheet_name='Área plantada (Hectares)')

        # for some reason only this column is int
        # to avoid errors and creating unnecessary handlers
        # I've added this type casting
        area_df["2008"] = area_df[2008].astype(str)

        self._set_attr_from_dataframe(area_df, self.data, 'area')

    def _set_production(self) -> None:
        production_df = pd.read_excel(self.xlsx_file, sheet_name='Quantidade produzida (Tonela...')
        self._set_attr_from_dataframe(production_df, self.data, 'production')

    def _set_attr_from_dataframe(self, df: Any, obj: dict, key: str) -> None:
        for index, row in df.iterrows():
            city = row['Município']
            city_data = {}

            if not isinstance(city, str):
                # this avoids to add a 'NaN' city
                continue

            if not obj.get(city):
                obj[city] = {}

            for year in self.range_years:
                row_value = row[str(year)]

                city_data[year] = {
                    key: row_value
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
        df_keys = ['area', 'production']

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

    def get_dataset(self) -> pd.DataFrame:
        self._set_area()
        self._set_production()
        self._handle_dataset_values()
        return self.dataframe

