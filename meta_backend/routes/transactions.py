from fastapi import APIRouter, Depends

from uuid import UUID
from typing import List

from configs import (
    get_current_user, 
    SessionDep, 
    get_keycloak_service,
    KeycloakUserService,
    check_roles
)
from controller import (
    load_transactions,
    load_transaction_by_id,
    create_transaction,
    update_transaction_by_id,
    delete_transaction_by_id
)
from models import (
    TransactionCreate,
    TransactionRead,
    TransactionUpdate
)
from utils import logger


transaction_v1_router = APIRouter(
    prefix="/api/v1/transaction",
    tags=['Transaction']
)

@transaction_v1_router.get(
        "/", 
        response_model=List[TransactionRead],
        dependencies=[Depends(check_roles(["Manager", "Admin"]))]
    )
async def get(
    session: SessionDep,
    user: dict = Depends(get_current_user),
    kc_service: KeycloakUserService = Depends(get_keycloak_service)
):
    return load_transactions(kc_service, session)


@transaction_v1_router.get("/{tx_id}", response_model=TransactionRead)
async def get_by_id(
    tx_id: UUID,
    session: SessionDep,
    kc_service: KeycloakUserService = Depends(get_keycloak_service),
    user: dict = Depends(get_current_user)
):
    return load_transaction_by_id(tx_id, kc_service, session)


@transaction_v1_router.post("/add", response_model=TransactionRead)
async def add(
    transaction: TransactionCreate, 
    session: SessionDep, 
    user: dict = Depends(get_current_user)
):
    return create_transaction(transaction, session)

@transaction_v1_router.put('/update/{coin_id}', response_model=TransactionRead)
async def update(
    transaction_id: UUID,
    transaction_update: TransactionUpdate, 
    session: SessionDep, 
    user: dict = Depends(get_current_user)
):
    return update_transaction_by_id(transaction_id, transaction_update, session)
    

@transaction_v1_router.delete("/{transaction_id}")
async def delete(
    transaction_id: UUID,
    session: SessionDep, 
    user: dict = Depends(get_current_user)
):
    return delete_transaction_by_id(transaction_id, session)