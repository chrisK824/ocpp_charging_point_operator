from datetime import datetime, timedelta
from ocpp.routing import on
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import Action, RegistrationStatus, AuthorizationStatus, TriggerMessageStatus
from ocpp.v16 import call_result
from random import randint
import logging
from sql_app import crud, models, schemas, database
from sql_app.database import SessionLocal

logging.basicConfig(filename='ocpp.log', level=logging.DEBUG)
LOGGER = logging.getLogger('ocpp')


class ChargePointHandler(cp):
    def __init__(self, charge_point_id, websocket):
        cp.__init__(self, charge_point_id, websocket)
        self.booted = False
        self.authorized = False
        self.transaction_id = None

    def create_id_tag_info(self, id_tag):
        id_tag_info = {}
        db = SessionLocal()
        id_tag_db = crud.get_idToken_of_charging_station(db, id_tag, self.id)
        db.close()
        if not id_tag_db:
            id_tag_info['status'] = AuthorizationStatus.invalid
        else:
            if datetime.strptime(id_tag_db.expiry_date, "%Y-%m-%dT%H:%M:%SZ") > datetime.utcnow():
                id_tag_info['status'] = AuthorizationStatus.accepted
                id_tag_info['expiry_date'] = id_tag_db.expiry_date
            else:
                id_tag_info['status'] = AuthorizationStatus.expired
            if id_tag_db.parent_token:
                id_tag_info['parent_id_tag'] = id_tag_db.parent_token
        return id_tag_info

    @on(Action.Authorize)
    def on_authorize(self, id_tag):
        id_tag_info = self.create_id_tag_info(id_tag)
        if id_tag_info.get('status') == AuthorizationStatus.accepted:
            self.authorized = True
        return call_result.AuthorizePayload(id_tag_info=id_tag_info)

    @on(Action.BootNotification)
    def on_boot_notitication(self, charge_point_vendor, charge_point_model, **kwargs):
        LOGGER.info('Substation %s booted up', self.id)
        self.booted = True
        return call_result.BootNotificationPayload(
            current_time=datetime.utcnow().isoformat(),
            interval=900,
            status=RegistrationStatus.accepted
        )

    @on(Action.Heartbeat)
    def on_heartbeat(self):
        LOGGER.info('Substation %s heartbeat sent', self.id)
        return call_result.HeartbeatPayload(
            current_time=datetime.utcnow().isoformat()
        )

    @on(Action.MeterValues)
    def on_meter_values(self, connector_id, meter_value):
        LOGGER.info(
            f'Substation {self.id} meter values sent from connector {connector_id}:')
        LOGGER.info(f'{meter_value}')
        return call_result.MeterValuesPayload()

    @on(Action.StartTransaction)
    def on_start_transaction(self, connector_id, id_tag, meter_start, timestamp, **kwargs):
        id_tag_info = self.create_id_tag_info(id_tag)
        # if not self.authorized:
        #     id_tag_info['status'] = AuthorizationStatus.expired ?
        if not self.transaction_id:
            self.transaction_id = randint(1, 10000)
        # else:
        #     return call_error ?
        return call_result.StartTransactionPayload(
            transaction_id=self.transaction_id,
            id_tag_info=id_tag_info
        )

    @on(Action.StopTransaction)
    def on_stop_transaction(self, meter_stop, timestamp, transaction_id, **kwargs):
        if kwargs.get("id_tag"):
            id_tag_info = self.create_id_tag_info(kwargs.get("id_tag"))
            if transaction_id == self.transaction_id:
                self.transaction_id = None
            # else:
            #     return call_error ?
            return call_result.StopTransactionPayload(
                id_tag_info=id_tag_info
            )
