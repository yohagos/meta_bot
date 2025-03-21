from typing import List, Union
from fastapi import APIRouter, Depends, Query
from uuid import UUID

from configs import get_current_user, SessionDep, KeycloakUserService, get_keycloak_service

from controller import (
    load_ci,
    load_ci_by_id,
    create_ci,
    update_ci_by_id,
    delete_ci_by_id
)

from models import (
    CoinInterestCreate,
    CoinInterestRead,
    CoinInterestUpdate,
    Stats
)

interest_v1_router = APIRouter(
    prefix="/api/v1/interest",
    tags=["Coin Interest"]
)

@interest_v1_router.get("/", response_model=List[CoinInterestRead])
async def get(
    session: SessionDep,
    user: dict = Depends(get_current_user),
    kc_service: KeycloakUserService = Depends(get_keycloak_service),
    offset: int = 0,
    limit: int = Query(default=100, le=100)
):
    return load_ci(kc_service, session, offset, limit)

@interest_v1_router.get("/{coin_id}", response_model=CoinInterestRead)
async def get_by_id(
    coin_id: UUID,
    session: SessionDep,
    user: dict = Depends(get_current_user),
    kc_service: KeycloakUserService = Depends(get_keycloak_service),
):
    return load_ci_by_id(coin_id, kc_service, session)

@interest_v1_router.post("/create", response_model=CoinInterestRead)
async def add(
    ci: Union[CoinInterestCreate | Stats],
    session: SessionDep,
    user: dict = Depends(get_current_user),
    kc_service: KeycloakUserService = Depends(get_keycloak_service),
):
    return create_ci(ci, session, kc_service)

@interest_v1_router.put("/update/{ci_id}", response_model=CoinInterestRead)
async def update(
    ci_id: UUID,
    ci: CoinInterestUpdate,
    session: SessionDep,
    user: dict = Depends(get_current_user),
    kc_service: KeycloakUserService = Depends(get_keycloak_service),
):
    return update_ci_by_id(ci_id, ci, kc_service, session)

@interest_v1_router.delete("/{ci_id}", response_model=CoinInterestRead)
async def delete(
    ci_id: UUID,
    session: SessionDep,
    user: dict = Depends(get_current_user),
    kc_service: KeycloakUserService = Depends(get_keycloak_service),
):
    return delete_ci_by_id(ci_id, session, kc_service)