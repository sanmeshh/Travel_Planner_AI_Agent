from pydantic import BaseModel
from typing import List,Optional
from schemas.preferences import BudgetRange,ActivityPreference

class ResolvedGroupPreference(BaseModel):
    final_location: Optional[str]
    final_budget: Optional[BudgetRange]
    destination_type: Optional[str]
    travel_style: Optional[str]
    activities: List[ActivityPreference]
    reasoning: str

    