from typing import List
from fastapi import APIRouter, Depends, Query
from uuid import UUID

from configs import get_current_user, SessionDep

from controller import (
    load_ch,
    load_ch_by_id,
    create_ch,
    update_ch,
    delete_ch_by_id
)

from models import (
    CoinHistoryCreate,
    CoinHistoryRead,
    CoinHistoryUpdate
)

history_v1_router = APIRouter(
    prefix="/api/v1/history",
    tags=["Coin History"]
)

@history_v1_router.get("/", response_model=List[CoinHistoryRead])
async def get(
    session: SessionDep,
    user: dict = Depends(get_current_user),
    offset: int = 0,
    limit: int = Query(default=100, le=100)
):
    return load_ch(session, offset, limit)

@history_v1_router.get("/{h_id}", response_model=CoinHistoryRead)
async def get_by_id(
    h_id: UUID,
    session: SessionDep,
    user: dict = Depends(get_current_user),
):
    return load_ch_by_id(h_id, session)

@history_v1_router.post("/create", response_model=CoinHistoryRead)
async def add(
    ch: CoinHistoryCreate,
    session: SessionDep,
    user: dict = Depends(get_current_user),
):
    return create_ch(ch, session)

@history_v1_router.put("/update/{h_id}", response_model=CoinHistoryRead)
async def update(
    h_id: UUID,
    h_update: CoinHistoryUpdate,
    session: SessionDep,
    user: dict = Depends(get_current_user),
):
    return update_ch(h_id, h_update, session)

@history_v1_router.delete("/{h_id}", response_model=CoinHistoryRead)
async def delete(
    h_id: UUID,
    session: SessionDep,
    user: dict = Depends(get_current_user),
):
    return delete_ch_by_id(h_id, session)