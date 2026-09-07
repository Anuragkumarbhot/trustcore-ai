from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse
from app.auth.dependencies import get_current_active_user
from app.services.authorization import require_permission

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.get("/", response_model=List[UserResponse])
async def list_users(
    _: User = Depends(require_permission("user:read")),
    db: Session = Depends(get_db)
):
    users = db.query(User).all()
    return users 