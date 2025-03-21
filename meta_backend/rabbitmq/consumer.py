import asyncio, json
from typing import Set, Optional
from fastapi.websockets import WebSocket

from configs import load_settings
from utils import logger
from . import rabbitmq_connection

settings = load_settings()

active_websocktes: Set[WebSocket] = set()

last_message: Optional[dict]

async def add_websocket(websocket: WebSocket):
    await websocket.accept()
    active_websocktes.add(websocket)
    global last_message

    if last_message is not None:
        try: 
            await websocket.send_json(last_message)
        except Exception:
            pass

    try:
        while True:
            message = await websocket.receive_text()
    except Exception:
        active_websocktes.remove(websocket)
    finally:
        active_websocktes.discard(websocket)


async def broadcast_data(data: dict):
    global last_message
    last_message = data
    disconnected_clients = set()

    for ws in active_websocktes:
        try: 
            await ws.send_json(data)
        except:
            disconnected_clients.add(ws)
    
    for ws in disconnected_clients:
        active_websocktes.remove(ws)
        

async def consume():
    await rabbitmq_connection.connect()
    channel = rabbitmq_connection.channel
    queue = await channel.get_queue(settings.MQ_QUEUE)

    async with queue.iterator() as queue_iter:
        while True:
            try:
                message = await queue_iter.__anext__()
                async with message.process():
                    data = json.loads(message.body.decode())
                    await broadcast_data(data)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.warning("error occurred in consume()")
                await asyncio.sleep(1)


async def start_consumer():
    asyncio.create_task(consume())