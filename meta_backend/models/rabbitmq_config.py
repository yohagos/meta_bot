from pydantic import BaseModel
from typing import List, Dict, Any
from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from sqlalchemy.types import JSON


class RabbitMQConfig(SQLModel, table=True):
    __tablename__ = "rabbitmq_config"
    __table_args__ = {"extend_existing": True}
    
    id: str = Field(default=str, primary_key=True, index=True, unique=True)
    exchange_name: str = Field(index=True, unique=True)
    exchange_type: str 
    queue_name: str = Field(index=True, unique=True)
    routing_key: str = Field(index=True, unique=True)
    durable: bool = True
    auto_delete: bool = False
    arguments: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))



