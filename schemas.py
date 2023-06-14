from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class IdToken(BaseModel):
    token: str
    expiry_date: datetime
    charging_substation_id: str

    class Config:
        orm_mode = True


class ChargingSubStationRegister(BaseModel):
    id: str
    connectors_number: Optional[int] = None
    vendor: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class ChargingSubStation(ChargingSubStationRegister):
    id_token: str

    class Config:
        orm_mode = True
