from fastapi import HTTPException, status
from sqlmodel import select
from uuid import UUID
from typing import List

from configs import (
    SessionDep, 
    KeycloakUserService
)
from models import (
    CoinHistory,
    CoinHistoryRead,
    CoinHistoryCreate,
    CoinHistoryUpdate
)

def load_ch(
    session: SessionDep,
    offset: int,
    limit: int
) -> List[CoinHistoryRead]:
    chs = session.exec(select(CoinHistory).offset(offset).limit(limit)).all()
    return [
        CoinHistoryRead.model_validate(
            ch,
            update={
                'coin': ch.coin
            }
        )
        for ch in chs
    ]

def load_ch_by_id(
    h_id: UUID,
    session: SessionDep
) -> CoinHistoryRead:
    ch = session.get(CoinHistory, h_id)
    if not ch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='CoinHistory not found'
        )
    return CoinHistoryRead.model_validate(
        ch,
        update={
            'coin': ch.coin
        }
    )

def create_ch(
    ch_create: CoinHistoryCreate,
    session: SessionDep
) -> CoinHistoryRead:
    db_ch = CoinHistory.model_validate(ch_create)
    session.add(db_ch)
    session.commit()
    session.refresh(db_ch)
    return CoinHistoryRead.model_validate(
        db_ch,
        update={
            'coin': db_ch.coin
        }
    )

def update_ch(
        h_id: UUID,
        ch_update: CoinHistoryUpdate,
        session: SessionDep
) -> CoinHistoryRead:
    if not h_id:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail='Id not provided'
        )
    ch = session.get(CoinHistory, h_id)
    if not ch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='CoinHistory not found'
        )
    
    update_data = ch_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if getattr(ch, key) != value:
            setattr(ch, key, value)

    session.add(ch)
    session.commit()
    session.refresh(ch)
    return CoinHistoryRead.model_validate(
        ch,
        update={
            'coin': ch.coin
        }
    )

def delete_ch_by_id(
    h_id: UUID,
    session: SessionDep
) -> CoinHistoryRead:
    if not h_id:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail='Id not provided'
        )
    ch = session.get(CoinHistory, h_id)
    if not ch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='CoinHistory not found'
        )
    session.delete(ch)
    session.commit()
    return CoinHistoryRead.model_validate(
        ch,
        update={
            'coin': ch.coin
        }
    )