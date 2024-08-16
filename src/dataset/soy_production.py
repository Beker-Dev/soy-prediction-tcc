from typing import Any

import pandas as pd
import json


class SoyProductionDataset:
    def __init__(self, xlsx_file: str = 'assets/tabela1612_mod.xlsx', range_years: range = range(2008, 2022 + 1)):
        self.xlsx_file = xlsx_file
        self.range_years = range_years
        self.data = dict()

    def _set_area(self):
        area_df = pd.read_excel(self.xlsx_file, sheet_name='Área plantada (Hectares)')

        # for some reason only this column is int
        # to avoid errors and creating unnecessary handlers
        # I've added this type casting
        area_df["2008"] = area_df[2008].astype(str)

        self._set_attr_from_dataframe(area_df, self.data, 'area')

    def _set_production(self):
        production_df = pd.read_excel(self.xlsx_file, sheet_name='Quantidade produzida (Tonela...')
        self._set_attr_from_dataframe(production_df, self.data, 'production')

    def _set_attr_from_dataframe(self, df: Any, obj: dict, key: str):
        for index, row in df.iterrows():
            city = row['Município']
            city_data = {}

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

    def _handle_empty_values(self):
        pass
        # if isinstance(row_value, str) and not row_value.isnumeric():
        #     # we probably should add some handler to insert a median value
        #     row_value = 0

    def get_dataset(self):
        self._set_area()
        self._set_production()
        self._handle_empty_values()
        return self.data


dataset = SoyProductionDataset('../assets/tabela1612_mod.xlsx')
dataset.get_dataset()
