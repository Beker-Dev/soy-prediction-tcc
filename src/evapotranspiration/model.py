from typing import Any

import pyet
import pandas as pd


class Evapotranspiration:
    def __init__(
            self,
            mean_temp: pd.Series,
            max_temp: float,
            min_temp: float,
            wind_speed: float,
            mean_humidity: float,
            solar_radiation: float,
            elevation: float
    ):
        self.mean_temp = mean_temp
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.wind_speed = wind_speed
        self.mean_humidity = mean_humidity
        self.solar_radiation = solar_radiation
        self.elevation = elevation

    def calculate(self) -> Any:
        return pyet.pm_fao56(
            tmean=self.mean_temp,
            tmax=self.max_temp,
            tmin=self.min_temp,
            wind=self.wind_speed,
            rh=self.mean_humidity,
            rs=self.solar_radiation,
            elevation=self.elevation
        )


evo = Evapotranspiration(
    pd.Series(data=[25.3, 25.9, 25.8, 26.9, 27, 27.5, 29.0, 31.3, 35.6]),
    35.6,
    25.3,
    10,
    40,
    8,
    1000
)

print(
    evo.calculate()
)
# it is not working :/