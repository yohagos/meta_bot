from fastapi import HTTPException, status
from sqlmodel import select
from uuid import UUID

from configs import (
    SessionDep, 
    KeycloakUserService
)
from models import (
    Transaction,
    TransactionCreate,
    TransactionRead,
    TransactionUpdate
)


def load_transactions(kc_service: KeycloakUserService ,session: SessionDep):
    transactions = session.exec(select(Transaction)).all()
    return [
        TransactionRead.model_validate(
            transaction,
            update={
                'user': kc_service.get_user_info(transaction.keycloak_user_id),
                'coin': transaction.coin
            }
        )
        for transaction in transactions
    ]

def load_transaction_by_id(
    tx_id: UUID, 
    kc_service: KeycloakUserService, 
    session: SessionDep
):
    tx = session.get(Transaction, tx_id)
    if not tx:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Transaction not found'
        )
    return TransactionRead.model_validate(
        tx,
        update={
            'user': kc_service.get_user_info(tx.keycloak_user_id),
            'coin': tx.coin
        }
    )

def create_transaction(
    transaction: TransactionCreate, 
    session: SessionDep,
):
    db_transaction = Transaction.model_validate(transaction)
    session.add(db_transaction)
    session.commit()
    session.refresh(db_transaction)
    return db_transaction

def update_transaction_by_id(
    transaction_id: UUID,
    transaction_update: TransactionUpdate, 
    session: SessionDep, 
):
    if not transaction_id:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail='Id not provided'
        )
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Coin not found'
        )
    update_data = transaction_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        if getattr(transaction, key) != value:
            setattr(transaction, key, value)
    
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction

def delete_transaction_by_id(
    transaction_id: UUID,
    session: SessionDep, 
):
    if not transaction_id:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail='Id not provided'
        )
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Transaction not found'
        )
    session.delete(transaction)
    session.commit()
    return transaction