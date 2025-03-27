from typing import Dict, Set
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.websockets import WebSocketState

from utils import logger

class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        self.connection_groups: Dict[WebSocket, str] = {}
    
    async def connect(
            self, 
            group: str, 
            websocket: WebSocket
    ) -> None:
        if websocket in self.active_connections:
            old_group = self.connection_groups[websocket]
            if old_group != group:
                self.disconnect(old_group, websocket)
        if group not in self.active_connections:
            self.active_connections[group] = set()
        self.active_connections[group].add(websocket)
        self.connection_groups[websocket] = group
    
    def disconnect(
            self,
            group: str,
            websocket: WebSocket
    ) -> None:
        if group in self.active_connections:
            self.active_connections[group].discard(websocket)
        if websocket in self.connection_groups:
            del self.connection_groups[websocket]
    
    async def broadcast(
            self,
            group: str,
            message: str
    ) -> None:
        if group not in self.active_connections:
            return
        
        for connection in list(self.active_connections[group]):
            try: 
                if connection.application_state != WebSocketState.CONNECTED:
                    self.disconnect(group, connection)
                    continue
                await connection.send_text(message)
            except (WebSocketDisconnect, RuntimeError) as e:
                logger.error(f"Error websocket or runtime : {str(e)}")
                self.active_connections[group].remove(connection)
            except Exception as e:
                logger.error(f"Error while broadcasting : {str(e)}")
                self.disconnect(group, connection)

