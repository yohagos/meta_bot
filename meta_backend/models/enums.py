from enum import Enum

class TransactionTypeEnum(str, Enum):
    SOLD = "SOLD"
    BOUGHT = "BOUGHT"


class WebSocketGroupsEnum(str, Enum):
    COINS = "COINS"
    TRANSACTIONS = "TRANSACTIONS"