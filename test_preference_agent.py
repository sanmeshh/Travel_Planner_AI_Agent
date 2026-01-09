from agents.preference_collector import collect_preferences
from llm_wrapper import llm

tests = [
    ("user1", "Budget 20 to 25k, Goa trip, relaxed, beaches and cafes in July"),
    ("user2", "Fun trip near Mumbai with water parks and amusement parks under 30k"),
    ("user3", "Hill station,flexible budget, adventure and trekking,August")
]

for uid, text in tests:
    prefs = collect_preferences(llm ,uid, text)
    print(prefs.model_dump())
