from datetime import datetime
from ocpp.routing import on
from ocpp.v16 import ChargePoint
from ocpp.v16.enums import Action, RegistrationStatus, AuthorizationStatus
from ocpp.v16 import call_result
from random import randint
import logging
import db_crud
from database import SessionLocal

logging.basicConfig(filename='ocpp.log', level=logging.DEBUG)
logger = logging.getLogger('ocpp')


class ChargePointHandler(ChargePoint):
    def __init__(self, charge_point_id, websocket):
        ChargePoint.__init__(self, charge_point_id, websocket)
        self.booted = False
        self.authorized = False
        self.transaction_id = None
        self.id_tag_info = None

    def update_id_tag_info(self, id_tag):
        id_tag_info = {}
        db = SessionLocal()
        id_tag_stored = db_crud.get_id_token_of_charging_station(db, self.id)
        db.close()
        if not id_tag_stored or id_tag_stored != id_tag:
            id_tag_info['status'] = AuthorizationStatus.invalid
        else:
            if datetime.strptime(id_tag_stored.expiry_date, "%Y-%m-%dT%H:%M:%SZ") > datetime.utcnow():
                id_tag_info['status'] = AuthorizationStatus.accepted
                id_tag_info['expiry_date'] = id_tag_stored.expiry_date
            else:
                id_tag_info['status'] = AuthorizationStatus.expired

        self.id_tag_info = id_tag_info

    @on(Action.Authorize)
    def on_authorize(self, id_tag):
        self.update_id_tag_info(id_tag)
        if self.id_tag_info.get('status') == AuthorizationStatus.accepted:
            self.authorized = True
        return call_result.AuthorizePayload(id_tag_info=self.id_tag_info)

    @on(Action.BootNotification)
    def on_boot_notitication(self, **kwargs):
        self.booted = True
        return call_result.BootNotificationPayload(
            current_time=datetime.utcnow().isoformat(),
            interval=900,
            status=RegistrationStatus.accepted
        )

    @on(Action.Heartbeat)
    def on_heartbeat(self):
        return call_result.HeartbeatPayload(
            current_time=datetime.utcnow().isoformat()
        )

    @on(Action.MeterValues)
    def on_meter_values(self, **kwargs):
        return call_result.MeterValuesPayload()

    @on(Action.StartTransaction)
    def on_start_transaction(self, id_tag, **kwargs):
        if not self.transaction_id:
            self.transaction_id = randint(1, 10000)

        self.update_id_tag_info(id_tag)

        return call_result.StartTransactionPayload(
            transaction_id=self.transaction_id,
            id_tag_info=self.id_tag_info
        )

    @on(Action.StopTransaction)
    def on_stop_transaction(self, transaction_id, **kwargs):
        if kwargs.get("id_tag"):
            self.update_id_tag_info(kwargs.get("id_tag"))
            if transaction_id == self.transaction_id:
                self.transaction_id = None
            return call_result.StopTransactionPayload(
                id_tag_info=self.id_tag_info
            )
