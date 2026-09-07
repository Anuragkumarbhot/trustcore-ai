from pydantic import BaseModel
from datetime import datetime

class CapabilityBase(BaseModel):
    code: str
    name: str
    description: str | None = None
    provider_name: str
    is_available: bool = True
    requires_approval: bool = False

class CapabilityCreate(CapabilityBase):
    pass

class CapabilityResponse(CapabilityBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True 