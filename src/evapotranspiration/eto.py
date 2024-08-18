from src.evapotranspiration import penmon as pm

import pandas as pd


class ETo:
    def __init__(self):
        pass

    @staticmethod
    def calculate_eto(
            latitude: float,
            altitude: int,
            date: str,  # YYYY-MM-DD
            temp_min: float,
            temp_max: float,
            temp_avg: float,
            wind_speed: float,
            humidity: float,
            radiation: float,
    ):
        station = pm.Station(latitude=latitude, altitude=altitude)
        day = station.day_entry(
            day_number=station.day_entry(date).day_number,
            temp_mean=temp_avg,
            temp_min=temp_min,
            temp_max=temp_max,
            wind_speed=wind_speed,
            humidity_mean=humidity,
            radiation_s=radiation
        )
        return day.eto()

