from typing import List
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission

def get_user_permissions(user: User) -> List[str]:
    """Return a set of permission names for the user (flattened from roles)."""
    permissions = set()
    for role in user.roles:
        for perm in role.permissions:
            permissions.add(perm.name)
    return list(permissions)

def has_permission(user: User, permission: str) -> bool:
    """Check if user has a specific permission."""
    return permission in get_user_permissions(user)

def require_permission(permission: str):
    """FastAPI dependency to require a permission."""
    from fastapi import Depends, HTTPException, status
    from app.auth.dependencies import get_current_user

    def dependency(user: User = Depends(get_current_user)):
        if not has_permission(user, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing required permission: {permission}"
            )
        return user
    return dependency