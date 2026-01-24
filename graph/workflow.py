from langgraph.graph import StateGraph
from graph.state import TripState
from agents.conflict_resolver import resolve_group
from schemas.preferences import UserPreference

def resolve(state: TripState):
    # reconstruct Pydantic models ONLY here
    prefs = [
        UserPreference(**p)
        for p in state.preferences.values()
    ]

    result = resolve_group(prefs)

    # store as dict ONLY
    state.resolved = result.model_dump()

    return state.model_dump()

builder = StateGraph(TripState)

# ✅ use YOUR resolve function
builder.add_node("resolve", resolve)

builder.set_entry_point("resolve")
builder.set_finish_point("resolve")

app = builder.compile()

