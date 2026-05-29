# api/ws_manager.py

from fastapi import WebSocket
import json


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"Client connected. Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"Client disconnected. Total: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        """Push a message to every connected browser."""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                # Connection died — mark it for cleanup
                disconnected.append(connection)
        for conn in disconnected:
            self.active_connections.remove(conn)

    async def send_to(self, websocket: WebSocket, message: dict):
        """Send a message to one specific client."""
        await websocket.send_json(message)


manager = ConnectionManager()