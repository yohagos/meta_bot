from typing import Optional
from datetime import datetime, timezone
from uuid import uuid4, UUID
from sqlmodel import SQLModel, Field
from pydantic import ConfigDict
from sqlalchemy import Column, DateTime, func

from .coins import Coin
from .coin_stats import Stats


class CoinInterestBase(SQLModel):
    keycloak_user_id: UUID
    coin_id: Optional[UUID] = Field(default=None)
    stats_id: Optional[str]= Field(default=None)

class CoinInterest(CoinInterestBase, table=True):
    __tablename__ = "coin_interest"
    __table_args__ = {"extend_existing": True}
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, index=True)
    created_date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )


class CoinInterestCreate(CoinInterestBase):
    pass

class CoinInterestRead(CoinInterestBase):
    id: UUID
    created_date: datetime

    coin: Optional[Coin] = None
    stats: Optional[Stats] = None

    model_config = ConfigDict(from_attributes=True)

class CoinInterestUpdate(SQLModel):
    coin_id: Optional[UUID] = None
    stats_id: Optional[str] = None

