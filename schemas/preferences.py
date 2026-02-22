from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class BudgetRange(BaseModel):
    min_budget: Optional[int] = None
    max_budget: Optional[int] = None

class UserPreference(BaseModel):
    user_id: str
    preferred_location: Optional[str] = None  # general preference
    budget: Optional[BudgetRange]
    trip_type: Optional[str] = None
    activities: List[str]
    startdate: Optional[date] = None
    enddate:Optional[date]=None
    
