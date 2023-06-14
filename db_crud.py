from sqlalchemy.orm import Session
import models, schemas
import uuid
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError


class DuplicateError(Exception):
    pass


def register_charging_substation(db: Session, charging_substation_register: schemas.ChargingSubStationRegister):
    charging_substation_to_add = models.ChargingSubStation(
        id=charging_substation_register.id,
        connectors_number=charging_substation_register.connectors_number,
        vendor=charging_substation_register.vendor,
        model=charging_substation_register.model,
        serial_number=charging_substation_register.serial_number,
        latitude=charging_substation_register.latitude,
        longitude=charging_substation_register.longitude
    )
    id_token_to_add = models.IdToken(
        token=uuid.uuid4(),
        expiry_date=datetime.utcnow() + timedelta(weeks=12),
        charging_substation_id=charging_substation_register.id
    )
    try:
        db.add(charging_substation_to_add)
        db.add(id_token_to_add)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise DuplicateError(
            f"Charging point already exists!")


def get_charging_substations(db: Session):
    return list(db.query(models.ChargingSubStation).all())


def get_charging_substation(db: Session, charging_substation_id: str):
    return db.query(models.ChargingSubStation).filter(
        models.ChargingSubStation.id == charging_substation_id).first()


def get_idToken_of_charging_station(db: Session, id_tag: str, charging_substation_id: str):
    return db.query(models.idToken).join(
        models.ChargingSubStation
    ).filter(
        models.idToken.token == id_tag
    ).filter(
        models.ChargingSubStation.id == charging_substation_id).first()

# TODO: add function to refresh token expiration date