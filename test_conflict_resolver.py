from schemas.preferences import UserPreference, BudgetRange, ActivityPreference
from agents.conflict_resolver import resolve_group

def test_resolve_group_basic():
    prefs = [
        UserPreference(
            user_id="u1",
            preferred_location="Goa",
            budget=BudgetRange(min_budget=1000, max_budget=3000),
            activities=[
                ActivityPreference(name="beach"),
                ActivityPreference(name="cafes"),
            ],
        ),
        UserPreference(
            user_id="u2",
            preferred_location="Manali",
            budget=BudgetRange(min_budget=1500, max_budget=2500),
            activities=[
                ActivityPreference(name="beach"),
                ActivityPreference(name="trekking"),
            ],
        ),
    ]

    result = resolve_group(prefs)

    print("=== RESULT TYPE ===")
    print(type(result))

    print("\n=== ACTIVITIES ===")
    for a in result.activities:
        print(a, type(a), type(a.name))

    print("\n=== MODEL DUMP ===")
    dumped = result.model_dump()
    print(dumped)

    print("\n=== DUMPED ACTIVITIES ===")
    for a in dumped["activities"]:
        print(a, type(a), type(a["name"]))


if __name__ == "__main__":
    test_resolve_group_basic()
