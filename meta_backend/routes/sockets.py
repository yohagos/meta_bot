from fastapi import APIRouter
from fastapi.websockets import WebSocket
from uuid import uuid4
from datetime import datetime

from rabbitmq import add_websocket
from models import Stats

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
        supply=19000000.0,
        maxSupply=21000000.0,
        marketCapUsd=800000000000.0,
        volumeUsd24Hr=30000000000.0,
        priceUsd=42000.5,
        changePercent24Hr=0.5,
        vwap24Hr=41500.0,
        timestamp=datetime.utcnow()
    )

@sockets_v1_router.get("/ws-docs", include_in_schema=True)
async def websoclet_docs():
    return {"info": "Websocket connection: ws://localhost:8000/api/v1/sockets/coins"}

@sockets_v1_router.websocket('/coins')
async def coins_assets(
    websocket: WebSocket
):
    await add_websocket(websocket)
