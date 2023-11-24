from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError

from lib_backend_console.globals import BackendConsoleGlobals


def websocket_server(app: FastAPI):
    @app.websocket("/sd-webui-backend-console")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        try:
            while True:
                message = await BackendConsoleGlobals.queue.get()
                await websocket.send_json(message)
        except (WebSocketDisconnect, ConnectionClosedOK, ConnectionClosedError):
            pass
