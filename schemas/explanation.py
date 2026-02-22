from pydantic import BaseModel
from typing import List,Dict,Optional,Any

class ExplanationSection(BaseModel):
    title:str
    summary:str
    details:Optional[List[str]]=None

class DecisionExplanation(BaseModel):
    overview: str
    location: ExplanationSection
    budget: ExplanationSection
    
    activities: ExplanationSection 
    dates: ExplanationSection
    trip_type:ExplanationSection
    
    excluded_preferences: Dict[str, Any] 
    voting_summary: Dict[str, Any]
    
