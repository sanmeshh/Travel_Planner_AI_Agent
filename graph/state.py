from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any

class TripState(BaseModel):
    users: List[str] = Field(default_factory=list)
    preferences: Dict[str, dict] = Field(default_factory=dict)
    ready_users: List[str] = Field(default_factory=list)

    expected_users: int | None = None   # 👈 NEW
    resolved: Optional[dict] = None
