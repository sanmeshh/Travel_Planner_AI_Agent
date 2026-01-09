from agents.preference_collector import collect_preferences
from llm_wrapper import llm
from agents.conflict_resolver import resolve_group

def collect_node(state):
    user = state.current_user
    msg = state.current_message.lower()

    if "done" in msg or "ready" in msg:
        state.ready_users.add(user)
        return state

    new_pref = collect_preferences(llm, user, state.current_message)

    if user in state.preferences:
        old = state.preferences[user]
        merged = old.model_copy(update=new_pref.model_dump(exclude_none=True))
        state.preferences[user] = merged
    else:
        state.preferences[user] = new_pref

    return state



def resolve_node(state):
    prefs = list(state.preferences.values())
    state.resolved = resolve_group(prefs)
    return state



