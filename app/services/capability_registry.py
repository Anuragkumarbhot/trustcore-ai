from sqlalchemy.orm import Session
from app.models.capability import Capability
from typing import List, Optional

class CapabilityRegistry:
    """In-memory registry that also persists to database."""

    def __init__(self, db: Session):
        self.db = db
        self._capabilities = self._load_from_db()

    def _load_from_db(self) -> List[Capability]:
        return self.db.query(Capability).all()

    def get_by_code(self, code: str) -> Optional[Capability]:
        for cap in self._capabilities:
            if cap.code == code:
                return cap
        return None

    def get_all(self) -> List[Capability]:
        return self._capabilities

    def register(self, capability: Capability) -> Capability:
        self.db.add(capability)
        self.db.commit()
        self.db.refresh(capability)
        self._capabilities.append(capability)
        return capability