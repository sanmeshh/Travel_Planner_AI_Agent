from graph.workflow import app

state = {
    "users": ["u1", "u2"],
    "preferences": {},
    "ready_users": set()
}

# u1
state = app.invoke({**state, "current_user": "u1", "current_message": "Goa, 20k-30k, beaches"})

# u2
state = app.invoke({**state, "current_user": "u2", "current_message": "Near Mumbai, cheap, water park"})

# u1 done
state = app.invoke({**state, "current_user": "u1", "current_message": "done"})

# u2 done → triggers resolve
state = app.invoke({**state, "current_user": "u2", "current_message": "done"})

print(state["resolved"].model_dump())
