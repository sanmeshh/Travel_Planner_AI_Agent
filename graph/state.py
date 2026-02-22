from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any

class TripState(BaseModel):
    users: List[str] = Field(default_factory=list)
    preferences: Dict[str, dict] = Field(default_factory=dict)
    ready_users: List[str] = Field(default_factory=list)

    expected_users: Optional[int] = None  
    resolved: Optional[dict] = None
    itinerary:Optional[List[dict]]=None
