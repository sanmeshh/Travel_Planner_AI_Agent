from pydantic import BaseModel
from typing import List, Optional
from schemas.preferences import BudgetRange
from datetime import date

class PreferenceInput(BaseModel):
    budget: Optional[BudgetRange] = None
    preferred_location: Optional[str] = None
    trip_type: Optional[str] = None
    activities: List[str] = []   
    startdate: Optional[date] = None
    enddate:Optional[date]=None

    
