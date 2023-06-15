from sqlalchemy.orm import Session
import models, schemas
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
import string
import random


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

    try:
        db.add(charging_substation_to_add)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise DuplicateError(
            f"Charging point already exists!")

    return charging_substation_to_add


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


def create_id_token(db: Session, id_token_assign: schemas.IdTokenAssign):
    DEFAULT_EXPIRATION_WEEKS = 12
    charging_substation = db.query(
        models.ChargingSubStation).filter(
        models.ChargingSubStation.id == id_token_assign.charging_substation_id).first()
    
    if not charging_substation:
        raise ValueError(f"There is no charging substation with ID: {id_token_assign.charging_substation_id}")
    
    if id_token_assign.expiry_date is not None:
        expiration_date = id_token_assign.expiry_date
    else:
        expiration_date = datetime.utcnow() + timedelta(weeks=DEFAULT_EXPIRATION_WEEKS)

    letters = string.ascii_lowercase
    token = ''.join(random.choice(letters) for i in range(20))

    id_token_to_add = models.IdToken(
        token=token,
        expiry_date=expiration_date,
        charging_substation_id=id_token_assign.charging_substation_id
    )
    try:
        db.add(id_token_to_add)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise DuplicateError(
            f"ID token already exists, please try again!")

    return id_token_to_add


def get_id_token(db: Session, charging_substation_id: str):
    id_token = db.query(models.IdToken).filter(
        models.IdToken.charging_substation_id == charging_substation_id).first()
    if not id_token:
        raise ValueError(f"No ID token found for charging substation with ID: {charging_substation_id}")
    return id_token


def refresh_id_token(db: Session, charging_substation_id: str):
    DEFAULT_EXPIRATION_WEEKS = 12
    id_token = db.query(
        models.IdToken).filter(
        models.IdToken.charging_substation_id == charging_substation_id).first()
    
    if not id_token:
        raise ValueError(f"There is no ID token for charging substation with ID: {charging_substation_id}")
    
    expiration_date = datetime.utcnow() + timedelta(weeks=DEFAULT_EXPIRATION_WEEKS)

    id_token.expiry_date = expiration_date
    db.commit()
    return id_token