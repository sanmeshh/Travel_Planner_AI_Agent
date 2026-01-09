from agents.conflict_resolver import resolve_group
from schemas.preferences import UserPreference, BudgetRange, ActivityPreference

prefs = [
    UserPreference(
        user_id="u1",
        preferred_location="Goa",
        budget=BudgetRange(min_budget=20000, max_budget=30000),
        activities=[ActivityPreference(name="beaches"), ActivityPreference(name="cafes")]
    ),
    UserPreference(
        user_id="u2",
        preferred_location="Goa",
        budget=BudgetRange(min_budget=25000, max_budget=40000),
        activities=[ActivityPreference(name="beaches"), ActivityPreference(name="water_park")]
    )
]

print(resolve_group(prefs).model_dump())
