from pydantic import BaseModel, Field
from typing import List, Optional

class BudgetRange(BaseModel):
    min_budget: Optional[int] = None
    max_budget: Optional[int] = None

class ActivityPreference(BaseModel):
    name: str  # water_park, amusement_park, trekking, etc.
    specific_place: Optional[str] = None  # e.g. "Imagica", "Wet N Joy"

class UserPreference(BaseModel):
    user_id: str
    preferred_location: Optional[str] = None  # general preference
    budget: Optional[BudgetRange]
    destination_type: Optional[str] = None
    travel_style: Optional[str] = None
    activities: List[ActivityPreference] = Field(default_factory=list)
    dates: Optional[str] = None
    
