
from pydantic import BaseModel
from typing import List, Dict, Optional
from schemas.preferences import BudgetRange
from datetime import date

class ResolvedGroupPreference(BaseModel):
    final_location: Optional[str]
    final_budget: BudgetRange
    trip_type: Optional[str]
    activities: List[str]
    final_start_date: date
    final_end_date: date
    total_days: int
    excluded_preferences: Dict[str, List[str]]
    reasoning: Dict[str, str]
    votes: Dict[str, Dict[str, int]]



    