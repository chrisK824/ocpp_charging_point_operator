import asyncio, json, logging
from websockets.exceptions import ConnectionClosed
from starlette.websockets import WebSocket
from charge_point_handler import ChargePointHandler
from typing import List
from fastapi import Depends, FastAPI
from utils import WebSocketInterface
import uvicorn
from sql_app import db_crud, models, schemas, database
from sqlalchemy.orm import Session
from sql_app.database import engine
from contextlib import asynccontextmanager

logging.basicConfig(filename='ocpp.log',level=logging.DEBUG)
logger = logging.getLogger('ocpp')

@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=engine)
    yield


async def on_connect(websocket, charge_point_id):
    """
    For every new charge point that connects, create a ChargePoint instance
    and start listening for messages.
    """
    cp = ChargePointHandler(charge_point_id, websocket)
    try:
        await cp.start()
    except ConnectionClosed as err:
        logger.info(f'Connection from charging point with ID {cp.id} was closed. Info: {err.rcvd}')


app = FastAPI(
    title='Charging Point Operator API',
    version="0.0.1",
    lifespan=lifespan
)


@app.get("/charging_points", response_model=List[schemas.ChargingSubStation])
def get_active_charging_points(db: Session = Depends(database.get_db)):
    return db_crud.get_charging_substations(db)


@app.websocket('/ocpp1.6/{charge_point_id}')
async def websocket_listener(websocket_obj: WebSocket, charge_point_id: str, db: Session = Depends(database.get_db)):
    if db_crud.get_charging_substation(db, charge_point_id):
        await websocket_obj.accept()
        standard_ws = WebSocketInterface(websocket_obj)
        await on_connect(standard_ws, charge_point_id)
    else:
        logger.error(f"No charging point registration found for ID {charge_point_id}")
        await websocket_obj.close()

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=9999)