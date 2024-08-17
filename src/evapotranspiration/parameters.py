from enum import Enum


class Parameters(Enum):
    T2M_MAX_AVG: "Temperature at 2 Meters Maximum Average"
    T2M_MAX: "Temperature at 2 Meters Maximum"
    T2M_MIN: "Temperature at 2 Meters Minimum"
    ALLSKY_SFC_SW_DWN: "All Sky Surface Shortwave Downward Irradiance"
    RH2M: "Relative Humidity at 2 Meters"
    WS2M: "Wind Speed at 2 Meters"
