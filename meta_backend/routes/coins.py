from typing import List
from fastapi import APIRouter, Depends, Query
from uuid import UUID

from configs import get_current_user, SessionDep
from controller import (
    load_coins,
    load_coin_by_id,
    create_coin,
    update_coin,
    delete_coin_by_id
)
from models import (
    CoinCreate,
    CoinRead,
    CoinUpdate
)
from services import fetch_coin_data


coins_v1_router = APIRouter(
    prefix="/api/v1/coins",
    tags=['Coins']
)

@coins_v1_router.get("/fetch-data")
async def fetch_data():
    data = await fetch_coin_data()
    return data


@coins_v1_router.get("/", response_model=List[CoinRead])
async def get(
    session: SessionDep,
    user: dict = Depends(get_current_user),
    offset: int = 0,
    limit: int = Query(default=100, le=100)
):
    return load_coins(session, offset, limit)


@coins_v1_router.get("/{coin_id}", response_model=CoinRead)
async def get_by_id(
    coin_id: UUID,
    session: SessionDep,
    user: dict = Depends(get_current_user)
):
    return load_coin_by_id(coin_id, session)


@coins_v1_router.post("/create", response_model=CoinRead)
async def add(
    coin: CoinCreate, 
    session: SessionDep, 
    user: dict = Depends(get_current_user)
):
    return create_coin(coin, session)


@coins_v1_router.put('/update/{coin_id}', response_model=CoinRead)
async def update(
    coin_id: UUID,
    coin_update: CoinUpdate, 
    session: SessionDep, 
    user: dict = Depends(get_current_user)
):
    return update_coin(coin_id, coin_update, session)
    

@coins_v1_router.delete("/{coin_id}")
async def delete(
    coin_id: UUID,
    session: SessionDep, 
    user: dict = Depends(get_current_user)
):
    return delete_coin_by_id(coin_id, session)




