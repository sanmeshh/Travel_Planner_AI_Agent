# from llm_wrapper import llm

# sys_prompt="""You are an Explanation Agent for a deterministic group decision system.

# Your task is to EXPLAIN an already-made decision.
# You MUST NOT make decisions, suggestions, or changes.

# Rules you must follow:
# - Use ONLY the information provided in the input.
# - DO NOT invent preferences, votes, or reasons.
# - DO NOT optimize or critique the decision.
# - If information is missing, explicitly state that it was unavailable.
# - Keep explanations clear, neutral, and factual.
# - Output must match the required structured format.

# You are explaining the system’s behavior to end users."""

# user_prompt="""
# Here is the final group decision and supporting metadata.

# Decision JSON:
# {decision_json}

# Resolution Rules:
# - Budget was resolved using intersection of all user budget ranges.
# - Location was resolved using majority voting with deterministic tie-breaks.
# - Activities were resolved using majority voting with fallback.

# Vote Summary:
# {votes}

# Excluded Preferences:
# {excluded_preferences}

# Explain the decision clearly for a general user.

# """

# response=llm.invoke(sys_prompt,user_prompt)

# print(response)

from schemas.explanation import DecisionExplanation, ExplanationSection

def generate_explanation(
    resolved_decision: dict,
    votes: dict,
    excluded_preferences: dict
) -> DecisionExplanation:
    """
    Read-only explanation generator.
    No decisions are made here.
    """

    #Overview 
    overview = (
        "The group trip was finalized using predefined rules such as "
        "majority voting and budget intersection to ensure fairness."
    )

    #Location 
    location_value = resolved_decision.get("final_location")

    location_section = ExplanationSection(
        title="Location Selection",
        summary=(
            f"{location_value} was selected because it received the highest number "
            "of votes among the group.If there is tie the location is chosen alphabetically."
            if location_value
            else "No single location preference dominated the group decision."
        ),
        details=[
            f"{loc}: {count} vote(s)"
            for loc, count in votes.get("location", {}).items()
        ] or None
    )

    #Budget
    budget = resolved_decision.get("final_budget", {})

    budget_section = ExplanationSection(
        title="Budget Resolution",
        summary=(
            "The final budget range was chosen so that it fits within "
            "everyone’s specified limits."
            if budget.get("min_budget") or budget.get("max_budget")
            else "No common budget range could be found for all users."
        ),
        details=[
            f"Minimum budget: {budget.get('min_budget')}",
            f"Maximum budget: {budget.get('max_budget')}",
        ] if budget else None
    )

   #Activities
    activities = resolved_decision.get("activities", [])

    #Extract just the names if they are dictionaries
    activity_names = [(a.get("name")).title() if isinstance(a, dict) else a for a in activities]

    activities_section = ExplanationSection(
        title="Activity Selection",
        summary=(
            f"The group chose {', '.join(activity_names)} based on interest."
            if activity_names else "No activities selected."
        ),
        details=[
            f"{act}: {votes.get('activities', {}).get(act, 0)} vote(s)"
            for act in activity_names
        ] or None
    )

    #dates
    start=resolved_decision.get("final_start_date")
    end=resolved_decision.get("final_end_date")

    dates_section = ExplanationSection(
        title="Travel Dates",
        summary=(
            f"The trip is set for {start} to {end}. This range was determined "
            "by finding the smallest window where everyone is available."
        
        ),
        details=[f"Start: {start}", f"End: {end}"] if start else None
    )

    #Trip Type
    trip_type = resolved_decision.get("trip_type")
    
    trip_type_section = ExplanationSection(
        title="Trip Vibe",
        summary=f"The group agreed on a {trip_type} style for this journey." if trip_type else "General trip style.",
        details=None
    )


    return DecisionExplanation(
        overview=overview,
        location=location_section,
        budget=budget_section,
        activities=activities_section,
        dates=dates_section,      
        trip_type=trip_type_section,
        excluded_preferences=excluded_preferences,
        voting_summary=votes
    )



