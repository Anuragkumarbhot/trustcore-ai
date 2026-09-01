from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.audit_log import AuditLog
from app.schemas.audit import AuditLogResponse
from app.auth.dependencies import get_current_active_user
from app.services.authorization import require_permission

router = APIRouter(prefix="/audit", tags=["audit"])

@router.get("/", response_model=List[AuditLogResponse])
async def get_audit_logs(
    _: User = Depends(require_permission("audit:read")),
    db: Session = Depends(get_db)
):
    logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(100).all()
    return logs