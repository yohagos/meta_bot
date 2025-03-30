from fastapi import APIRouter, HTTPException, status
from fastapi.websockets import WebSocket
from uuid import uuid4
from datetime import datetime
from typing import Annotated, List
from sqlmodel import select

from configs import AsyncSessionDep
from models.coin_stats import Stats
from models.rabbitmq_config import RabbitMQConfig
from services import WebSocketManager
from utils import logger


sockets_v1_router = APIRouter(
    prefix="/api/v1/sockets",
    tags=['Sockets']
)

@sockets_v1_router.get("/socket-example", response_model=Stats)
async def get_example():
    return Stats(
        id=uuid4(),
        data_id="btc-bitcoin",
        name="Bitcoin",
        symbol="BTC",
        rank="1",
        explorer="https://blockchain.com",
        supply=19_000_000.0,
        maxSupply=21_000_000.0,
        marketCapUsd=800_000_000_000.0,
        volumeUsd24Hr=30_000_000_000.0,
        priceUsd=42_000.5,
        changePercent24Hr=0.5,
        vwap24Hr=41_500.0,
        timestamp=datetime.utcnow()
    )

@sockets_v1_router.get("/ws-docs", include_in_schema=True)
async def websoclet_docs():
    return {"info": "Websocket connection: ws://localhost:8000/api/v1/sockets/coins"}


@sockets_v1_router.get("/groups")
async def consumer_groups(
    session: AsyncSessionDep
):
    groups = await session.exec(select(RabbitMQConfig))
    if groups is None:
        return []
    ids = [group.id for group in groups]
    return ids


@sockets_v1_router.websocket("/ws/all")
async def websocket(
    websocket: WebSocket
):
    await websocket.accept()

    ws_manager = websocket.app.state.ws_manager
    await ws_manager.connect('all', websocket)

    try:
        while True:
            await websocket.receive_text()
    except Exception as e:
        logger.error(f"Websocket error : {str(e)}")
        ws_manager.disconnect('all', websocket)
    
