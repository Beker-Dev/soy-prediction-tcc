from enum import Enum


class ParametersRequest(Enum):
    # these will be requested in nasa power api
    T2M = "Temperature at 2 Meters"
    ALLSKY_SFC_SW_DWN = "All Sky Surface Shortwave Downward Irradiance"
    RH2M = "Relative Humidity at 2 Meters"
    WS2M = "Wind Speed at 2 Meters"


class Parameters(Enum):
    # these will be used to calculate ETo
    T2M = "Temperature at 2 Meters"
    T2M_MAX = "Temperature at 2 Meters Maximum"
    T2M_MIN = "Temperature at 2 Meters Minimum"
    ALLSKY_SFC_SW_DWN = "All Sky Surface Shortwave Downward Irradiance"
    RH2M = "Relative Humidity at 2 Meters"
    WS2M = "Wind Speed at 2 Meters"

    # this one is to keep ETo
    ETO = "Evapotranspiration"
