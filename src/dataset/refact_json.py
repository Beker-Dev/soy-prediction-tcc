from typing import Any

import pandas as pd
import json

xlsx_file = 'assets/tabela1612_mod.xlsx'
excel_file = pd.ExcelFile(xlsx_file)
range_years = range(2008, 2022 + 1)
data = {}


def set_area():
    area_df = pd.read_excel(xlsx_file, sheet_name='Área plantada (Hectares)')

    # for some reason only this column is int
    # to avoid errors and creating unnecessary handlers
    # I've added this type casting
    area_df["2008"] = area_df[2008].astype(str)
    
    set_attr_from_dataframe(area_df, data, 'area')


def set_production():
    production_df = pd.read_excel(xlsx_file, sheet_name='Quantidade produzida (Tonela...')
    set_attr_from_dataframe(production_df, data, 'production')


def set_attr_from_dataframe(df: Any, obj: dict, key: str, ):
    for index, row in df.iterrows():
        city = row['Município']
        city_data = {}

        if not obj.get(city):
            obj[city] = {}

        for year in range_years:
            row_value = row[str(year)]

            if isinstance(row_value, str) and not row_value.isnumeric():
                # we probably should add some handler to insert a median value
                row_value = 0

            city_data[year] = {
                key: row_value
            }
        else:
            for ano, dados in city_data.items():
                if ano in obj[city]:
                    obj[city][ano].update(dados)
                else:
                    obj[city][ano] = dados


set_area()
set_production()

