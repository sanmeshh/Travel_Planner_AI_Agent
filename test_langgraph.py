from graph.state import TripState
from graph.workflow import app
from schemas.preferences import UserPreference, ActivityPreference, BudgetRange

# 1. Prepare your data first
users_list = ["u1", "u2"]
ready_users_list = ["u1", "u2"]

preferences_data = {
    "u1": UserPreference(
        user_id="u1",
        budget=BudgetRange(min_budget=1000, max_budget=2000),
        preferred_location="Goa",
        activities=[ActivityPreference(name="beach", specific_place=None)],
    ),
    "u2": UserPreference(
        user_id="u2",
        budget=BudgetRange(min_budget=1500, max_budget=2500),
        preferred_location="Goa",
        activities=[ActivityPreference(name="beach", specific_place=None)],
    )
}

# 2. Build the state inside the constructor
state = TripState(
    users=users_list,
    ready_users=ready_users_list,
    preferences=preferences_data
)

# 3. Run LangGraph
# Note: LangGraph's app.invoke usually takes a DICT that matches the state schema
result = app.invoke(state.model_dump()) 

print("RAW RESULT:", result)

