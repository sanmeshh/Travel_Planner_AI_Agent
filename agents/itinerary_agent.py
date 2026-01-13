from llm_wrapper import llm

def generate_itinerary(group_pref):
    prompt = f"""
You are a travel planner.

Given this group decision:
{group_pref.model_dump()}

Generate a 3-day itinerary with:
- morning
- afternoon
- evening

Return JSON in this format:
{{
  "day1": {{ "morning": "", "afternoon": "", "evening": "" }},
  "day2": ...
}}
"""
    return llm.invoke(prompt)