from sqlalchemy.orm import Session

from . import models, schemas


def get_charging_substation(db: Session, charging_substation_id: str):
    return db.query(models.ChargingSubStation).filter(models.ChargingSubStation.id == charging_substation_id).first()

def get_list_of_charging_substations(db: Session, charging_substations_ids: list):
    return db.query(models.ChargingSubStation).filter(models.ChargingSubStation.id.in_(charging_substations_ids)).all()

def get_idToken_of_charging_station(db: Session, id_tag: str, charging_substation_id: str):
    return db.query(models.idToken).join(models.ChargingSubStation).filter(models.idToken.token==id_tag).filter(models.ChargingSubStation.id==charging_substation_id).first()

def get_charging_substations(db: Session):
    return db.query(models.ChargingSubStation).all()