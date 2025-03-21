from typing import Optional
from uuid import uuid4, UUID
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, func
from pydantic import ConfigDict

from models.coins import Coin, CoinRead
from models.user import User
from models.enums import TransactionTypeEnum


class TransactionBase(SQLModel):
    keycloak_user_id: UUID
    coin_id: UUID = Field(foreign_key="coin_base.id")
    transaction_type: TransactionTypeEnum
    amount: float
    price: float

class Transaction(TransactionBase, table=True):
    __tablename__ = "transaction"
    __table_args__ = {"extend_existing": True}
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, index=True)
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )

    coin: Coin = Relationship(sa_relationship_kwargs={'lazy': 'joined'})
    

class TransactionCreate(TransactionBase):
    pass

class TransactionRead(TransactionBase):
    id: UUID
    timestamp: datetime
    user: Optional[User] = None

    coin: CoinRead

    model_config = ConfigDict(from_attributes=True)


class TransactionUpdate(SQLModel):
    transaction_type: TransactionTypeEnum
    amount: Optional[float] = None
    price: Optional[float] = None