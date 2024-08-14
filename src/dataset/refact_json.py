import pandas as pd
import json

xlsx_file = 'assets/tabela1612_mod.xlsx'

excel_file = pd.ExcelFile(xlsx_file)
area_df = pd.read_excel(xlsx_file, sheet_name='Área plantada (Hectares)')
producao_df = pd.read_excel(xlsx_file, sheet_name='Quantidade produzida (Tonela...')

data = {}
range_years = range(2008, 2022 + 1)

# for some reason only this column is int
# to avoid errors and creating unnecessary handlers
# I've added this type casting
area_df["2008"] = area_df[2008].astype(str)

print(area_df.columns)
# print(producao_df.columns)

for index, row in area_df.iterrows():
    city = row['Município']
    city_data = {}

    for year in range_years:
        area = row[str(year)]

        if isinstance(area, str) and not area.isnumeric():
            # we probably should add some handler to insert a median value
            area = 0

        city_data[year] = {
            'area': area
        }
    else:
        data[city] = city_data
else:
    print('data', data)

