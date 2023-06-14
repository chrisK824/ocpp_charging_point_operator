from sqlalchemy.orm import Session
import models


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

# TODO: add function to register a charging substation