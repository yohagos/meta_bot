from typing import Optional
from datetime import datetime, timezone
from uuid import uuid4, UUID
from sqlmodel import SQLModel, Field, Relationship
from pydantic import ConfigDict
from sqlalchemy import Column, DateTime, func

from models.coins import CoinRead, Coin
from models.transactions import Transaction, TransactionRead


class CoinHistoryBase(SQLModel):
    coin_id: UUID = Field(foreign_key="coin_base.id")
    price: float
    volume: Optional[float] = None
    market_cap: Optional[float] = None
    transaction_id: UUID = Field(foreign_key="transaction.id")
    

class CoinHistory(CoinHistoryBase, table=True):
    __tablename__ = "coin_history"
    __table_args__ = {"extend_existing": True}
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, index=True)
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )

    coin: Coin = Relationship(sa_relationship_kwargs={'lazy': 'joined'})
    transaction: Transaction = Relationship(sa_relationship_kwargs={'lazy': 'joined'})

class CoinHistoryCreate(CoinHistoryBase):
    pass

class CoinHistoryRead(CoinHistoryBase):
    id: UUID
    timestamp: datetime

    coin: CoinRead
    transaction: TransactionRead
    model_config = ConfigDict(from_attributes=True)

class CoinHistoryUpdate(SQLModel):
    price: Optional[float] = None
    volume: Optional[float] = None
    market_cap: Optional[float] = None
