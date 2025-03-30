from fastapi import HTTPException, status
from sqlmodel import select, or_, and_
from uuid import UUID
from typing import List, Tuple

from configs import (
    SessionDep, 
    KeycloakUserService
)
from models import (
    CoinInterest,
    CoinInterestCreate,
    CoinInterestRead,
    CoinInterestUpdate,
    Stats,
    Coin
)

from utils import logger

def load_ci(
    kc_service: KeycloakUserService,
    session: SessionDep,
    offset: int,
    limit: int
) -> List[CoinInterestRead]:
    cis = session.exec(select(CoinInterest).offset(offset).limit(limit)).all()
    return [
        CoinInterestRead.model_validate(
            ci,
            update={
                'user': kc_service.get_user_info(ci.keycloak_user_id),
                'coin': _findCoinByCoinId(session, ci.coin_id),
                'stats': _findStatsByStatsId(session, ci.stats_id)
            }
        )
        for ci in cis
    ]

def load_ci_by_id(
        ci_id: UUID,
        kc_servicce: KeycloakUserService,
        session: SessionDep,
):
    ci = session.get(CoinInterest, ci_id)
    if not ci:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='CoinInterest not found'
        )
    return CoinInterestRead.model_validate(
        ci,
        update={
            'user': kc_servicce.get_user_info(ci.keycloak_user_id),
            'coin': _findCoinByCoinId(session, ci.coin_id),
            'stats': _findStatsByStatsId(session, ci.stats_id)
        }
    )

def _findCoinByCoinId(session: SessionDep, id: UUID) -> Coin | None:
    coin = session.exec(select(Coin).where(Coin.id==id)).first()
    if coin:
        return coin
    return None

def _findStatsByStatsId(session: SessionDep, id: str) -> Stats | None:
    stats = session.exec(select(Stats).where(Stats.data_id==id)).first()
    if stats:
        return stats
    return None

def create_ci(
    ci:  CoinInterestCreate,
    session: SessionDep,
    kc_service: KeycloakUserService
) -> CoinInterestRead:
    if not ci.coin_id and not ci.stats_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No Coin or Stats was declared"
        )
    
    coin : Tuple[Coin | UUID] | None = None
    stats : Tuple[Stats | UUID] | None = None
    db_ci = CoinInterest.model_validate(ci)

    if ci.coin_id:
        coin = session.exec(select(Coin).where(Coin.id==ci.coin_id)).first()
        if not coin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Coin {ci.coin_id} not found"
            )
    if ci.stats_id:
        stats = session.exec(select(Stats).where(Stats.data_id==ci.stats_id)).first()
        if not stats:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Stats {ci.stats_id} not found"
            )
    
    session.add(db_ci)
    session.commit()
    session.refresh(db_ci)
    return CoinInterestRead.model_validate(
        db_ci,
        update={
            'user': kc_service.get_user_info(db_ci.keycloak_user_id),
            'stats': stats if stats is not None else None,
            'coin': coin if coin is not None else None
        }
    )
    

def update_ci_by_id(
    ci_id: UUID,
    ci_update: CoinInterestUpdate,
    kc_service: KeycloakUserService,
    session: SessionDep
) -> CoinInterestRead:
    if not ci_id:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail='Id not provided'
        )
    ci = session.get(CoinInterest, ci_id)
    if not ci:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='CoinInterest not found'
        )
    update_data = ci_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        if getattr(ci, key) != value:
            setattr(ci, key, value)

    session.add(ci)
    session.commit()
    session.refresh(ci)
    return CoinInterestRead.model_validate(
        ci,
        update={
            'user': kc_service.get_user_info(ci.keycloak_user_id),
            'coin': ci.coin
        }
    )


def delete_ci_by_id(
    ci_id: UUID,
    session: SessionDep
) -> CoinInterestRead:
    if not ci_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Id not provided'
        )
    ci = session.exec(select(CoinInterest).where(CoinInterest.id == ci_id)).first()
    if not ci:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='CoinInterest not found'
        )
    response = CoinInterestRead.model_validate(ci)
    session.delete(ci)
    session.commit()
    return response