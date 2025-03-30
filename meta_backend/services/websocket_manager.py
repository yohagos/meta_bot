from typing import Dict, Set
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.websockets import WebSocketState

from utils import logger

class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
    
    async def connect(
            self, 
            group: str, 
            websocket: WebSocket
    ) -> None:
        if group not in self.active_connections:
            self.active_connections[group] = set()
        self.active_connections[group].add(websocket)
    
    def disconnect(
            self,
            group: str,
            websocket: WebSocket
    ) -> None:
        if group in self.active_connections:
            self.active_connections[group].discard(websocket)
    
    async def broadcast(
            self, 
            group: str, 
            message: str
    ) -> None:
        if group not in self.active_connections:
            return
        for connection in list(self.active_connections[group]):
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Broadcast error: {e}")
                self.disconnect(group, connection)
