from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from schemas.input import PreferenceInput
from schemas.preferences import UserPreference
from schemas.group_preferences import ResolvedGroupPreference
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

# -----------------------------
# Submit Preferences
# -----------------------------
@app.post("/submit_preferences")
def submit(session_id: str, user_id: str, data: PreferenceInput):
    if session_id not in sessions:
        sessions[session_id] = TripState(expected_users=2)

    state = sessions[session_id]

    if user_id not in state.users:
        state.users.append(user_id)

    # 🔥 BUILD Pydantic model, THEN dump to dict
    pref = UserPreference(
        user_id=user_id,
        budget=data.budget,
        preferred_location=data.preferred_location,
        destination_type=data.destination_type,
        travel_style=None,
        activities=data.activities,
        dates=data.dates,
    )

    # 🔥 store RAW DICT ONLY
    state.preferences[user_id] = pref.model_dump()

    return {"status": "saved"}

@app.post("/create_session")
def create_session(session_id: str, expected_users: int):
    sessions[session_id] = TripState(
        expected_users=expected_users
    )
    return {"status": "created"}



# -----------------------------
# Mark Ready / Resolve
# -----------------------------
@app.post("/ready")
def ready(session_id: str, user_id: str):
    if session_id not in sessions:
        return {"status": "error", "message": "No preferences submitted yet"}

    state = sessions[session_id]

   
    if user_id not in state.ready_users:
        state.ready_users.append(user_id)

    # Resolve only when everyone is ready
    if (
    state.expected_users is not None
    and len(state.users) == state.expected_users
    and set(state.ready_users) == set(state.users)
):
        raw = agent.invoke(state.model_dump())

        # rebuild TripState ONCE
        state = TripState(**raw)
        sessions[session_id] = state

        # 🔥 rebuild Pydantic ONLY at response boundary
        final = ResolvedGroupPreference(**state.resolved)
        return {"status": "final", "result": final}

    return {
        "status": "waiting",
        "ready": state.ready_users,
        "users": state.users,
    }


@app.get("/sessions")
def debug_sessions():
    return sessions
