from fastapi import status, HTTPException
from sqlmodel import select
from uuid import UUID
from typing import List

from configs import SessionDep
from models import (
    CoinCreate,
    CoinRead,
    Coin,
    CoinUpdate
)

def load_coins(
    session: SessionDep,
    offset: int,
    limit: int
) -> List[CoinRead]:
    coins = session.exec(select(Coin).offset(offset).limit(limit)).all()
    return [
        CoinRead.model_validate(coin)
        for coin in coins
    ]

def load_coin_by_id(
    coin_id: UUID,
    session: SessionDep
) -> CoinRead:
    coin = session.get(Coin, coin_id)
    if not coin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coin not found"
        )
    return coin

def create_coin(
    coin: CoinCreate, 
    session: SessionDep
):
    db_coin = Coin.model_validate(coin)
    session.add(db_coin)
    session.commit()
    session.refresh(db_coin)
    return db_coin

def update_coin(
    coin_id: UUID,
    coin_update: CoinUpdate, 
    session: SessionDep
):
    if not coin_id:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail='Id not provided'
        )
    coin = session.get(Coin, coin_id)
    if not coin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Coin not found'
        )
    update_data = coin_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        if getattr(coin, key) != value:
            setattr(coin, key, value)
    
    session.add(coin)
    session.commit()
    session.refresh(coin)
    return coin

def delete_coin_by_id(
    coin_id: UUID,
    session: SessionDep
):
    if not coin_id:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail='Id not provided'
        )
    coin = session.get(Coin, coin_id)
    if not coin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Coin not found'
        )
    session.delete(coin)
    session.commit()
    return coin