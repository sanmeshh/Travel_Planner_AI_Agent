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

#init the sessions
sessions: dict[str, TripState] = {}

#create session
def get_session(session_id: str) -> TripState:
    if session_id not in sessions:
        sessions[session_id] = TripState()
    return sessions[session_id]


#submit the preferences
@app.post("/submit_preferences")
def submit_preferences(session_id: str, user_id: str, data: PreferenceInput):
    state = get_session(session_id)

    #wont accept new users after lock
    if state.expected_users is not None and user_id not in state.users:
        return {
            "status": "error",
            "message": "Group is locked. No new users allowed."
        }

    if user_id not in state.users:
        state.users.append(user_id)

   
    pref = UserPreference(
        user_id=user_id,
        budget=data.budget,
        preferred_location=data.preferred_location,
        destination_type=data.destination_type,
        travel_style=None,
        activities=data.activities,
        dates=data.dates,
    )

    #storinf raw dict
    state.preferences[user_id] = pref.model_dump()

    return {"status": "saved"}



#lock group 
@app.post("/lock_group")
def lock_group(session_id: str):
    if session_id not in sessions:
        return {"status": "error", "message": "Session not found"}

    state = sessions[session_id]

    if state.expected_users is not None:
        return {"status": "already_locked"}

    state.expected_users = len(state.users)

    return {
        "status": "locked",
        "expected_users": state.expected_users
    }



#Mark ready and resolve
@app.post("/ready")
def mark_ready(session_id: str, user_id: str):
    if session_id not in sessions:
        return {"status": "error", "message": "Session not found"}

    state = sessions[session_id]

    if user_id not in state.users:
        return {
            "status": "error",
            "message": "User has not submitted preferences"
        }

    if user_id not in state.ready_users:
        state.ready_users.append(user_id)

    print(
        f"[SESSION {session_id}] "
        f"users={state.users}, "
        f"ready={state.ready_users}, "
        f"expected={state.expected_users}"
    )

    #Resolve when,group is locked,users are ready and not already resolved
    if (
        state.expected_users is not None
        and len(state.users) == state.expected_users
        and set(state.ready_users) == set(state.users)
        and state.resolved is None
    ):
        raw = agent.invoke(state.model_dump())
        state = TripState(**raw)
        sessions[session_id] = state

        final = ResolvedGroupPreference(**state.resolved)
        return {"status": "final", "result": final}

    return {
        "status": "waiting",
        "ready": state.ready_users,
        "users": state.users,
        "expected_users": state.expected_users,
    }


@app.get("/sessions")
def debug_sessions():
    return sessions
