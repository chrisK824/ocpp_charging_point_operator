from starlette.websockets import WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosed

# transform starlette websocket to standard websocket
class WebSocketInterface():
    def __init__(self, websocket: WebSocket):
        self._websocket = websocket

    async def recv(self) -> str:
        try:
            return await self._websocket.receive_text()
        except WebSocketDisconnect as e:
            raise ConnectionClosed(e.code, 'WebSocketInterface')

    async def send(self, msg: str) -> None:
        await self._websocket.send_text(msg)

    async def close(self):
        await self._websocket.close()