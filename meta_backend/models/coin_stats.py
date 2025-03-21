from typing import Optional
from datetime import datetime
from uuid import uuid4, UUID
from sqlmodel import SQLModel, Field

class CoinStats(SQLModel):
    data_id: str = Field(index=True, unique=True)
    name: str = Field(index=True, unique=True)
    symbol: str = Field(index=True, unique=True)
    rank: str = Field(index=True, unique=True)
    explorer: Optional[str]
    supply: Optional[float]
    maxSupply: Optional[float]
    marketCapUsd: Optional[float]
    volumeUsd24Hr: Optional[float]
    priceUsd: Optional[float]
    changePercent24Hr: Optional[float]
    vwap24Hr: Optional[float]

class Stats(CoinStats, table=True):
    __tablename__ = "coin_stats"
    __table_args__ = {'extend_existing': True}
    
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, index=True)
    timestamp: datetime
