from typing import List, Optional

from pydantic import BaseModel


class idToken(BaseModel):
    token: str
    parent: bool
    user: str
    parent_token: str
    expiry_date: str
    charging_substation_id: str

    class Config:
        orm_mode = True



class ChargingSubStation(BaseModel):
    id: str
    connectors_number: int
    vendor: str
    model: str
    serial_number: str
    latitude: float
    longitude: float

    class Config:
        orm_mode = True
