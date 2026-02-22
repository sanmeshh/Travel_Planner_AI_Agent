from typing import List, Dict, Tuple
from collections import Counter
import math
from schemas.preferences import (
    UserPreference,
    BudgetRange)
from schemas.group_preferences import ResolvedGroupPreference
from datetime import date,timedelta


# -----------------------------
# Budget Resolution (Intersection)
# -----------------------------
def resolve_budget(preferences: List[UserPreference]) -> BudgetRange:
    mins, maxs = [], []

    for p in preferences:
        if p.budget:
            if p.budget.min_budget is not None:
                mins.append(p.budget.min_budget)
            if p.budget.max_budget is not None:
                maxs.append(p.budget.max_budget)

    if not mins or not maxs:
        return BudgetRange(min_budget=None, max_budget=None)

    final_min = max(mins)
    final_max = min(maxs)

    # No overlap → unresolved conflict
    if final_min > final_max:
        return BudgetRange(min_budget=None, max_budget=None)

    return BudgetRange(min_budget=final_min, max_budget=final_max)


# -----------------------------
# Location Resolution (Voting + deterministic tie-break)
# -----------------------------
def resolve_location(preferences: List[UserPreference]) :
    locations = [p.preferred_location.lower() for p in preferences if p.preferred_location]
    
    if not locations:
        return None, {}

    counter = Counter(locations)
    max_votes = max(counter.values())

    winners = [loc for loc, c in counter.items() if c == max_votes]

    # Deterministic tie-break: alphabetical
    final_location = sorted(winners)[0]

    return final_location, dict(counter)

def resolve_trip(preferences:List[UserPreference]):
    types = [p.trip_type.lower() for p in preferences if p.trip_type]
    if not types:
        return "Not Specified"
    

    counter = Counter(types)
    return counter.most_common(1)[0][0]



# Activity Resolution 
def resolve_activities(preferences: List[UserPreference],) -> Tuple[List[str], Dict[str, int]]:
    counter = Counter()
    user_count = len(preferences)

    for p in preferences:
        for a in p.activities:
            counter[a.lower()] += 1

    if not counter:
        return [], {}

    majority = math.ceil(user_count / 2)

    # Step 1: strict majority
    winners = [a for a, c in counter.items() if c >= majority]

    # Step 2: fallback to highest votes
    if not winners:
        max_votes = max(counter.values())
        winners = [a for a, c in counter.items() if c == max_votes]

    # Step 3: deterministic tie-break
    winners = sorted(winners)
    print(winners)

   

    return winners, dict(counter)


# -----------------------------
# Excluded Preferences (Structured)
# -----------------------------
def compute_excluded_preferences(
    preferences: List[UserPreference],
    final_activities: List[str],
) -> Dict[str, List[str]]:
    final_set = {a for a in final_activities}
    excluded: Dict[str, List[str]] = {}

    for p in preferences:
        for act in p.activities:
            if act not in final_set:
                excluded.setdefault(act, []).append(p.user_id)

    return excluded

def resolve_dates(preferences: List[UserPreference]):
    
    starts = [p.start_date for p in preferences if p.startdate]
    ends = [p.end_date for p in preferences if p.enddate]

    if not starts or not ends:
        return date.today(), date.today() + timedelta(days=1), 2

    final_start = max(starts)
    final_end = min(ends)

    # If there is NO overlap (the smallest range is negative)
    if final_start > final_end:
        # Fallback: Pick the range with the most common start date
        final_start = starts[0] 
        final_end = ends[0]
        # You should also add a note to 'reasoning' here!
    
    duration = (final_end - final_start).days + 1
    return final_start, final_end, duration

def resolve_group(preferences: List[UserPreference]) -> ResolvedGroupPreference:
    final_budget = resolve_budget(preferences)
    final_location, location_votes = resolve_location(preferences)
    final_activities, activity_votes = resolve_activities(preferences)
    
    #Actually resolve the trip type
    final_trip_type = resolve_trip(preferences)

    start,end,duration=resolve_dates(preferences)

    excluded_preferences = compute_excluded_preferences(
        preferences, final_activities
    )

    reasoning = {
        "budget": "Resolved using intersection of all user budget ranges.",
        "location": "Resolved using majority voting with deterministic tie-break.",
        "activities": "Resolved using majority voting with deterministic fallback.",
        "trip_type": f"Decided on {final_trip_type} based on most frequent user input."
    }

    return ResolvedGroupPreference(
        final_location=final_location,
        final_budget=final_budget.model_dump(), 
        trip_type=final_trip_type,        
        activities=final_activities,
        final_start_date=start,
        final_end_date=end,
        total_days=duration,
        excluded_preferences=excluded_preferences,
        reasoning=reasoning,
        votes={
            "location": location_votes,
            "activities": activity_votes,
        }
    )