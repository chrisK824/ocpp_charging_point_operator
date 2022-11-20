from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class idToken(Base):
    __tablename__ = 'id_tokens'

    token = Column(String, primary_key=True)
    parent = Column(Boolean)
    user = Column(String)
    parent_token = Column(String)
    expiry_date = Column(String)
    charging_substation_id = Column(String, ForeignKey('charging_substations.id'))
    charging_substation = relationship('ChargingSubStation')

    def __repr__(self):
        return f'idToken: {self.token}'

class ChargingSubStation(Base):
    __tablename__ = 'charging_substations'

    id = Column(String, primary_key=True)
    connectors_number = Column(Integer)
    vendor = Column(String)
    model = Column(String)
    serial_number = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    idTokens = relationship(idToken, overlaps="charging_substation")

    def __repr__(self):
        return f'Charging SubStation: {self.id}'