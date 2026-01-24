from typing import List, Dict, Tuple
from collections import Counter
import math

from schemas.preferences import (
    UserPreference,
    BudgetRange,
    ActivityPreference,
)
from schemas.group_preferences import ResolvedGroupPreference


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
def resolve_location(preferences: List[UserPreference]) -> Tuple[str | None, Dict[str, int]]:
    locations = [p.preferred_location for p in preferences if p.preferred_location]

    if not locations:
        return None, {}

    counter = Counter(locations)
    max_votes = max(counter.values())

    winners = [loc for loc, c in counter.items() if c == max_votes]

    # Deterministic tie-break: alphabetical
    final_location = sorted(winners)[0]

    return final_location, dict(counter)


# -----------------------------
# Activity Resolution (Majority → fallback → deterministic)
# -----------------------------
def resolve_activities(
    preferences: List[UserPreference],
) -> Tuple[List[ActivityPreference], Dict[str, int]]:
    counter = Counter()
    user_count = len(preferences)

    for p in preferences:
        for a in p.activities:
            counter[a.name] += 1

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

    activities = [
        ActivityPreference(name=w, specific_place=None)
        for w in winners
    ]

    return activities, dict(counter)


# -----------------------------
# Excluded Preferences (Structured)
# -----------------------------
def compute_excluded_preferences(
    preferences: List[UserPreference],
    final_activities: List[ActivityPreference],
) -> Dict[str, List[str]]:
    final_set = {a.name for a in final_activities}
    excluded: Dict[str, List[str]] = {}

    for p in preferences:
        for act in p.activities:
            if act.name not in final_set:
                excluded.setdefault(act.name, []).append(p.user_id)

    return excluded


# -----------------------------
# Group Resolution (Main Entry)
# -----------------------------
def resolve_group(preferences: List[UserPreference]) -> ResolvedGroupPreference:
    final_budget = resolve_budget(preferences)

    final_location, location_votes = resolve_location(preferences)

    final_activities, activity_votes = resolve_activities(preferences)

    excluded_preferences = compute_excluded_preferences(
        preferences, final_activities
    )

    reasoning = {
        "budget": "Resolved using intersection of all user budget ranges.",
        "location": "Resolved using majority voting with deterministic tie-break.",
        "activities": "Resolved using majority voting with deterministic fallback.",
    }

    return ResolvedGroupPreference(
        final_location=final_location,
        final_budget=final_budget,
        destination_type=None,
        travel_style=None,
        activities=final_activities,
        excluded_preferences=excluded_preferences,
        reasoning=reasoning,
        votes={
            "location": location_votes,
            "activities": activity_votes,
        },
    )
