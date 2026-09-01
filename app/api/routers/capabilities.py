from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.capability import Capability
from app.schemas.capability import CapabilityCreate, CapabilityResponse
from app.auth.dependencies import get_current_active_user
from app.services.authorization import require_permission
from app.services.capability_registry import CapabilityRegistry

router = APIRouter(prefix="/capabilities", tags=["capabilities"])

@router.get("/", response_model=List[CapabilityResponse])
async def list_capabilities(
    _: User = Depends(require_permission("capability:read")),
    db: Session = Depends(get_db)
):
    registry = CapabilityRegistry(db)
    return registry.get_all()

@router.post("/", response_model=CapabilityResponse, status_code=201)
async def register_capability(
    cap_data: CapabilityCreate,
    _: User = Depends(require_permission("capability:write")),
    db: Session = Depends(get_db)
):
    registry = CapabilityRegistry(db)
    if registry.get_by_code(cap_data.code):
        raise HTTPException(status_code=400, detail="Capability code already exists")
    new_cap = Capability(**cap_data.dict())
    return registry.register(new_cap) 