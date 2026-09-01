from pydantic import BaseModel
from datetime import datetime

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str | None = None
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True