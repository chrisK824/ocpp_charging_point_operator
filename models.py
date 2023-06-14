from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from database import Base


class ChargingSubStation(Base):
    __tablename__ = 'charging_substations'

    id = Column(String, primary_key=True)
    connectors_number = Column(Integer, nullable=True)
    vendor = Column(String, nullable=True)
    model = Column(String, nullable=True)
    serial_number = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    id_token = relationship("IdToken", back_populates="charging_substation", cascade="all,delete", passive_deletes=True)

    def __repr__(self):
        return f'Charging SubStation: {self.id}'


class IdToken(Base):
    __tablename__ = 'id_tokens'
    token = Column(String, primary_key=True)
    expiry_date = Column(DateTime)
    charging_substation_id = Column(String, ForeignKey("charging_substations.id", ondelete="CASCADE"))

    charging_substation = relationship("ChargingSubStation", back_populates="id_token")

    def __repr__(self):
        return f'idToken: {self.token}'
