from llm_wrapper import llm
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
import json

search_tool=TavilySearchResults(k=3)
def plan_itinerary(state:dict):
    resolved=state.get('resolved')

    query=f"top-rated venues and booking links for {resolved['activities']} in {resolved['final_location']} for a {resolved['trip_type']}"
    search_results=search_tool.invoke(query)
    sys_prompt = """
      You are a highly detailed Travel Concierge. You must plan the trip based on the provided search results.

      ### CRITICAL RULES:
      1. NO DUPLICATE LINKS: Every activity MUST have a unique, relevant URL found in the search results.
      2. GOOGLE MAPS: If a specific booking link isn't available, provide a Google Maps 'Place' link.
      3. LOGISTICS: Include 30-60 mins of 'Buffer/Travel Time' between distant locations.
      4. SPECIFICITY: Name actual top-rated venues (e.g., 'Sunny Da Dhaba') instead of generic descriptions.

      ### OUTPUT FORMAT:
      You MUST return a JSON object in this EXACT format. Do not include any text before or after the JSON.
      {
        "days": [
          {
            "day_number": 1,
            "theme": "Adventure & Water Sports",
            "activities": [
              {
                "time": "10:00 AM",
                "desc": "Detailed description of the activity including specific venue name",
                "link": "https://specific-link-to-venue.com"
              }
            ]
          }
        ]
      }
      Note: Ensure you use 'day_number' as the key, not 'day'.
      """
    
    user_prompt = f"""
    Search Results: {search_results}
    Plan a trip from {resolved['final_start_date']} to {resolved['final_end_date']}.
    Location: {resolved['final_location']}
    Vibe: {resolved['trip_type']}
    Budget: {resolved['final_budget']}



    DIVERSITY RULE: 
    - Do not suggest the same major venue (like Wet'nJoy) on multiple days. 
    - Use Day 1 for {resolved['activities'][0] if resolved['activities'] else 'Primary Activity'}.
    - Use Day 2 for nature, sightseeing, or a different activity.
    - Ensure the 'theme' of each day is distinct.

    """
    response_content = llm.invoke(sys_prompt, user_prompt)

    try:
      
        data = json.loads(response_content)
        return {"itinerary": data.get("days", [])}
    except Exception as e:
        print(f"Failed to parse itinerary: {e}")
        return {"itinerary": []}



    
