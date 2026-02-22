from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from schemas.input import PreferenceInput
from schemas.preferences import UserPreference
from schemas.group_preferences import ResolvedGroupPreference
from schemas.explanation import DecisionExplanation

from agents.explanation_agent import generate_explanation
from graph.state import TripState
from graph.workflow import app as agent



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

#id and tripstate object
sessions: dict[str, TripState] = {}


#creates a trip with a session id or you can say trip id
def get_session(session_id: str) -> TripState:
    if session_id not in sessions:
        sessions[session_id] = TripState()
    return sessions[session_id]



@app.post("/submit_preferences")
def submit_preferences(session_id: str, user_id: str, data: PreferenceInput):
    state = get_session(session_id)


    
    if state.expected_users is not None and user_id not in state.users:
        return {
            "status": "error",
            "message": "Group is locked. No new users allowed."
        }

    if user_id not in state.users:
        state.users.append(user_id)

    # Convert input -> model
    pref = UserPreference(
        user_id=user_id,
        budget=data.budget,
        preferred_location=data.preferred_location,
        trip_type=data.trip_type,
        activities=data.activities,
        startdate=data.startdate,
        enddate=data.enddate
    )

    #Store RAW dict only
    state.preferences[user_id] = pref.model_dump()

    return {"status": "saved"}



# Lock Group (Finalize users)
@app.post("/lock_group")
def lock_group(session_id: str):
    if session_id not in sessions:
        return {"status": "error", "message": "Session not found"}

    state = sessions[session_id]

    if state.expected_users is not None:
        return {"status": "already_locked"}

    if not state.users:
        return {
            "status": "error",
            "message": "Cannot lock group with zero users"
        }

    state.expected_users = len(state.users)

    return {
        "status": "locked",
        "expected_users": state.expected_users
    }

#Mark Ready and Resolve
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

    #Resolve exactly once
    if (
        state.expected_users is not None
        and len(state.users) == state.expected_users
        and set(state.ready_users) == set(state.users)
        and state.resolved is None
    ):
        # Langgraph resolution
        raw = agent.invoke(state.model_dump())
        state = TripState(**raw)
        sessions[session_id] = state

        #decision model 
        final_decision = ResolvedGroupPreference(**state.resolved)

        #Generate explanation (read-only)
        explanation = generate_explanation(
            resolved_decision=state.resolved,
            votes=state.resolved.get("votes", {}),
            excluded_preferences=state.resolved.get(
                "excluded_preferences", {}
            ),
        )

        return {
            "status": "final",
            "result": final_decision,
            "explanation": explanation,
        }

    return {
        "status": "waiting",
        "ready": state.ready_users,
        "users": state.users,
        "expected_users": state.expected_users,
    }



# Debug
@app.get("/sessions")
def debug_sessions():
    return sessions
