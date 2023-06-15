from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.sql import func


class ChargingSubStation(Base):
    __tablename__ = 'charging_substations'

    id = Column(String, primary_key=True)
    connectors_number = Column(Integer, nullable=True)
    vendor = Column(String, nullable=True)
    model = Column(String, nullable=True)
    serial_number = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    register_date = Column(DateTime, default=func.now())

    id_token = relationship("IdToken", back_populates="charging_substation", cascade="all,delete", passive_deletes=True)


class IdToken(Base):
    __tablename__ = 'id_tokens'
    token = Column(String, primary_key=True)
    expiry_date = Column(DateTime)
    charging_substation_id = Column(String, ForeignKey("charging_substations.id", ondelete="CASCADE"))
    register_date = Column(DateTime, default=func.now())
    last_updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    charging_substation = relationship("ChargingSubStation", back_populates="id_token")

