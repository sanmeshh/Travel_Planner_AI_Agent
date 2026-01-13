from pydantic import BaseModel
from typing import List, Optional

class PreferenceInput(BaseModel):
    budget_min: int
    budget_max: int
    location: Optional[str]
    destination_type: Optional[str]
    activities: List[str]
    dates: Optional[str]
