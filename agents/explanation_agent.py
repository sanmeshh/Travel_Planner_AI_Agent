from llm_wrapper import llm

def explain_decision(group_pref):
    prompt = f"""
Explain why this destination and activities were chosen.

Decision:
{group_pref.model_dump()}

Explain in simple English for users.
"""
    return llm.invoke(prompt)
