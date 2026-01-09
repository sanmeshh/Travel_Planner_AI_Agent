from typing import Dict, List, Optional,Set
from pydantic import BaseModel
from schemas.preferences import UserPreference
from schemas.group_preferences import ResolvedGroupPreference



class TripState(BaseModel):
    users: list[str]
    preferences: Dict[str, UserPreference] = {}
    ready_users: Set[str] = set()
    current_user: Optional[str] = None
    current_message: Optional[str] = None
    resolved: Optional[ResolvedGroupPreference] = None

