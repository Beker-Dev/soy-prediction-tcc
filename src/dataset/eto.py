from src.evapotranspiration import penmon as pm

import pandas as pd


class ETo:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def include_eto_to_df(self, ):
        station = pm.Station(latitude=41.42, altitude=109)

        day = station.day_entry(238,
                                temp_min=19.5,
                                temp_max=25.6,
                                wind_speed=2.5,
                                humidity_mean=65,
                                radiation_s=25.6
                                )
        print("ETo for this day is", day.eto())

