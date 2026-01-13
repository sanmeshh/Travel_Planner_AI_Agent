import json
from schemas.preferences import UserPreference
import re

def collect_preferences(llm, user_id: str, text: str) -> UserPreference:
    prompt = f"""


      Return ONLY valid JSON in this exact format:
      {{
        "user_id": "{user_id}",
        "preferred_location": string | null,
        "budget": {{
            "min_budget": number | null,
            "max_budget": number | null
        }} | null,
        "destination_type": "beach" | "hill" | "city" | "rural" | null,
        "travel_style": "relaxed" | "adventure" | "mixed" | null,
        "activities": [
        {{
          "name": string,
          "specific_place": string | null
        }}
        ],
        "dates": string | null
      }}

      Rules:
      - Budget must be in INR
      - If user gives approximate budget, infer reasonable min/max
      - Normalize activities into short keywords
      - Use these activity keywords when relevant:
        water_park, amusement_park, theme_park,
        trekking, beaches, cafes, sightseeing
      - If something is not mentioned, return null
      -return in proper JSON format

      - If a specific place is mentioned for an activity (e.g., Imagica, Wonderla),
        store it in activities[].specific_place
      - Do NOT duplicate the same place in preferred_location
      - preferred_location is only for general location preferences

      - Each activity must be an object with fields:
        {{ "name": <activity>, "specific_place": null or string }}
      - If no specific place is mentioned, use null



Text:
{text}
"""


    response = llm.invoke(prompt)

    # Extract JSON safely
    match = re.search(r"\{.*\}", response, re.DOTALL)

    if not match:
        raise ValueError("LLM did not return JSON")

    json_str = match.group(0)

    try:
        data = json.loads(json_str)
    except Exception:
        raise ValueError("LLM returned invalid JSON")

    return UserPreference(**data)#this dict(** -> to unpack the dict) is sent for validation
