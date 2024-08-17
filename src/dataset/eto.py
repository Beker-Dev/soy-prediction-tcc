from src.evapotranspiration import penmon as pm

import pandas as pd


class ETo:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def include_eto_to_df(self):
        station = pm.Station(latitude=41.42, altitude=109)

        day = station.day_entry(
            day_number=station.day_entry("2020-05-01").day_number,
            temp_min=19.5,
            temp_max=45.6,
            wind_speed=20.5,
            humidity_mean=15,
            radiation_s=9
        )
        print("ETo for this day is", day.eto())
