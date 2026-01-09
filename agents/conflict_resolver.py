from typing import List
from schemas.preferences import UserPreference, BudgetRange, ActivityPreference
from schemas.group_preferences import ResolvedGroupPreference
from collections import Counter


#solving the budget,activity and including voting conflict

def resolve_budget(preferences:List[UserPreference]):
    mins=[]
    maxs=[]

    for p in preferences:
        if p.budget:#if the user has given budget
            if p.budget.min_budget:
                mins.append(p.budget.min_budget)
            if p.budget.max_budget:
                maxs.append(p.budget.max_budget)

        
        final_min=max(mins) if mins else None
        final_max=min(maxs) if maxs else None

    return BudgetRange(min_budget=final_min,max_budget=final_max)


def resolve_location(preferences):
    locations = [p.preferred_location for p in preferences if p.preferred_location]
    if not locations:
        return None
    return Counter(locations).most_common(1)[0][0]

ACTIVITY_COST = {
    "beaches": 1,
    "trekking": 1,
    "cafes": 1,
    "sightseeing": 1,
    "water_park": 3,
    "amusement_park": 3,
    "theme_park": 3
}

def resolve_activities(preferences):
    counts = Counter()

    for p in preferences:
        for act in p.activities:
            counts[act.name] += 1

    if not counts:
        return []

    # Find max vote count
    max_votes = max(counts.values())

    # All activities that have the max votes
    tied = [name for name, c in counts.items() if c == max_votes]

    # If only one winner, use it
    if len(tied) == 1:
        return [ActivityPreference(name=tied[0], specific_place=None)]

    else:

        # Tie → break using cost
        cheapest = min(
            tied,
            key=lambda x: ACTIVITY_COST.get(x, 2)
        )

        return [ActivityPreference(name=cheapest, specific_place=None)]


def resolve_group(preferences: List[UserPreference]) -> ResolvedGroupPreference:
    final_budget = resolve_budget(preferences)
    final_location = resolve_location(preferences)
    final_activities = resolve_activities(preferences)

    excluded = []
    for p in preferences:
        for act in p.activities:
            if act.name not in [a.name for a in final_activities]:
                excluded.append(f"{p.user_id} wanted {act.name}")

    reasoning = "Decisions were made using majority voting for activities and intersection of budget ranges."

    return ResolvedGroupPreference(
        final_location=final_location,
        final_budget=final_budget,
        destination_type=None,
        travel_style=None,
        activities=final_activities,
        excluded_preferences=excluded,
        reasoning=reasoning
    )










