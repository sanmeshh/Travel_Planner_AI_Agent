


from pydantic import BaseModel
from typing import List, Dict, Optional
from schemas.preferences import BudgetRange, ActivityPreference

class ResolvedGroupPreference(BaseModel):
    final_location: Optional[str]
    final_budget: BudgetRange
    destination_type: Optional[str]
    travel_style: Optional[str]

    activities: List[ActivityPreference]

    excluded_preferences: Dict[str, List[str]]
    reasoning: Dict[str, str]

    votes: Dict[str, Dict[str, int]]


    