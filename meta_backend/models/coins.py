from typing import Optional
from datetime import datetime, timezone
from uuid import uuid4, UUID
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, func

class CoinBase(SQLModel):
    coin_symbol: str = Field(index=True, unique=True)
    coin_name: str
    description: Optional[str] = Field(default=None, nullable=True)
    website: Optional[str] = Field(default=None, nullable=True)

class Coin(CoinBase, table=True):
    __tablename__ = "coin_base"
    __table_args__ = {"extend_existing": True}
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, index=True)
    created_date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )

class CoinCreate(CoinBase):
    pass

class CoinRead(CoinBase):
    id: UUID
    created_date: datetime

class CoinUpdate(SQLModel):
    coin_name: Optional[str] = None
    coin_symbol: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None

class CoinView(CoinBase):
    current_price: Optional[float] = None



