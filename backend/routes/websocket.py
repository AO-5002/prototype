# routers/websocket.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from connection_manager import manager

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    await websocket.send_json({
        "type": "init",
        "nodes": [
            {
                "id": str(f),
                "position": {"x": i * 100, "y": i * 25},
                "data": {"label": f.name},
            }
            for i, f in enumerate(websocket.app.state.files)
        ],
        "edges": []
    })

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
