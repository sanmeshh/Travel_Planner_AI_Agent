from langgraph.graph import StateGraph, END
from graph.state import TripState
from graph.nodes import collect_node, resolve_node

graph = StateGraph(TripState)

graph.add_node("collect", collect_node)
graph.add_node("resolve", resolve_node)

graph.set_entry_point("collect")

def router(state):
    # If everyone is ready, finalize
    if len(state.ready_users) == len(state.users):
        return "resolve"
    # Otherwise just collect this message and stop
    return END

graph.add_conditional_edges("collect", router)
graph.add_edge("resolve", END)

app = graph.compile()
