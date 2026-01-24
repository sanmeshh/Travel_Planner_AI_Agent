from pydantic import BaseModel
from typing import List, Optional
from schemas.preferences import BudgetRange, ActivityPreference

class PreferenceInput(BaseModel):
    budget: Optional[BudgetRange] = None
    preferred_location: Optional[str] = None
    destination_type: Optional[str] = None
    activities: List[ActivityPreference] = []
    dates: Optional[str] = None
