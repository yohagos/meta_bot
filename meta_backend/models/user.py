from pydantic import BaseModel, ConfigDict
from typing import Optional

class User(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    firstName: str
    lastName: str
    email: Optional[str] | None = None

    