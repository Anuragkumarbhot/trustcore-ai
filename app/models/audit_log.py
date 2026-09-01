from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String, nullable=False)  # e.g., "CAPABILITY_EXECUTED", "LOGIN"
    target_type = Column(String, nullable=True)  # e.g., "capability"
    target_id = Column(String, nullable=True)
    details = Column(Text, nullable=True)  # JSON string
    ip_address = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())