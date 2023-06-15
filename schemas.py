from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class IdTokenAssign(BaseModel):
    expiry_date: Optional[datetime]
    charging_substation_id: str


class IdToken(IdTokenAssign):
    token: str
    register_date: datetime
    last_updated_at: datetime

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
    register_date: datetime

    class Config:
        orm_mode = True
