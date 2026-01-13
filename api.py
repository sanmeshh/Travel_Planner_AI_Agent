from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas.input import PreferenceInput
from schemas.preferences import UserPreference, ActivityPreference, BudgetRange
from graph.state import TripState
from graph.workflow import app as agent

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

sessions = {}

@app.post("/submit_preferences")
def submit(session_id: str, user_id: str, data: PreferenceInput):
    if session_id not in sessions:
        sessions[session_id] = TripState(users=[])

    state = sessions[session_id]

    if user_id not in state.users:
        state.users.append(user_id)

    state.preferences[user_id] = UserPreference(
        user_id=user_id,
        budget=BudgetRange(min_budget=data.budget_min, max_budget=data.budget_max),
        preferred_location=data.location,
        destination_type=data.destination_type,
        travel_style=None,
        activities=[ActivityPreference(name=a, specific_place=None) for a in data.activities],
        dates=data.dates
    )

    return {"status": "saved"}

@app.post("/ready")
def ready(session_id: str, user_id: str):
    state = sessions[session_id]
    if user_id not in state.ready_users:
        state.ready_users.append(user_id)

    new_state = agent.invoke(state)
    sessions[session_id] = new_state

    if new_state.resolved:
        return {"status": "final", "result": new_state.resolved.model_dump()}
    return {"status": "waiting"}
