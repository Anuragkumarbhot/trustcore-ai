from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Capability(Base):
    __tablename__ = "capabilities"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)  # e.g., "CAP-028"
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    provider_name = Column(String, nullable=False)  # e.g., "nmap"
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # optional scope restrictions
    requires_approval = Column(Boolean, default=False)