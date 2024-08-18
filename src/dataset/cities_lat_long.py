import pandas as pd
import json


def excel_to_json(
        excel_path='assets/cities_lat_long.xlsx',
        json_path='assets/cities_lat_long.json'
):
    df = pd.read_excel(excel_path)

    cities_dict = df.to_dict(orient='records')

    with open(json_path, 'w', encoding="utf-8") as json_file:
        json.dump(cities_dict, json_file, indent=4, ensure_ascii=False)

    print("Arquivo JSON criado com sucesso!")
