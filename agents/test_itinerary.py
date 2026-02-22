from datetime import date
from itinerary_agent import plan_itinerary
def test_itinerary_node():
    # Mocking the resolved state exactly as it comes from resolve_group
    mock_state = {
        "resolved": {
            "final_location": "Lonavla",
            "activities": ["Wet N Joy", "Tiger Point"],
            "trip_type": "Adventure",
            "final_budget": {"min_budget": 3000, "max_budget": 7000},
            "final_start_date": date(2026, 5, 10),
            "final_end_date": date(2026, 5, 12)
        }
    }

    print("--- 🚀 Testing Itinerary Node with Groq ---")
    result = plan_itinerary(mock_state)

    if result["itinerary"]:
        print("✅ Success! Itinerary generated.")
        for day in result["itinerary"]:
            print(f"Day {day['day_number']}: {day['theme']}")
            for act in day['activities']:
                print(f"  - {act['time']}: {act['desc']} ({act['link']})")
    else:
        print("❌ Failed: Itinerary is empty.")

if __name__ == "__main__":
    test_itinerary_node()