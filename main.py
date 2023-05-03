import asyncio, json, logging
import websockets
from websockets.exceptions import ConnectionClosed
from charge_point_handler import ChargePointHandler
from typing import Optional, List
from fastapi import Depends, FastAPI, HTTPException
from websocketInterface import WebSocketInterface
import uvicorn
from sql_app import crud, models, schemas, database
from sqlalchemy.orm import Session
from sql_app.database import SessionLocal, engine
models.Base.metadata.create_all(bind=engine)


logging.basicConfig(filename='ocpp.log',level=logging.DEBUG)
LOGGER = logging.getLogger('ocpp')

active_charging_points = []

async def on_connect(websocket, charge_point_id):
    """ For every new charge point that connects, create a ChargePoint instance
    and start listening for messages.

    """
    cp = ChargePointHandler(charge_point_id, websocket)
    active_charging_points.append(cp)
    try:
        await cp.start()
    except ConnectionClosed as err:
        # await cp._connection.close()
        LOGGER.info(f'connection from {cp.id} was closed. Info: {err.rcvd}')
        active_charging_points.remove(cp)
        del cp

app = FastAPI()

@app.get("/active_charging_points", response_model=List[schemas.ChargingSubStation])
def get_active_charging_points(db: Session = Depends(database.get_db)):
    print([x.id for x in active_charging_points])
    charging_points = crud.get_list_of_charging_substations(db, charging_substations_ids= [x.id for x in active_charging_points])
    return charging_points

@app.websocket_route('/ocpp1.6/{charge_point_id:path}')
async def websocket_handler(websocket):
    charging_point_registry = False
    db = SessionLocal()
    charging_point_registry = crud.get_charging_substation(db, websocket.path_params['charge_point_id'])
    db.close()
    if charging_point_registry:
        interface = WebSocketInterface(websocket)
        await websocket.accept()
        await on_connect(interface, websocket.path_params['charge_point_id'])
    else:
        print(f"Not found {websocket.path_params['charge_point_id']}")
        await websocket.close()

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=9999)