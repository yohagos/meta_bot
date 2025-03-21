from enum import Enum

class TransactionTypeEnum(str, Enum):
    SOLD = "SOLD"
    BOUGHT = "BOUGHT"