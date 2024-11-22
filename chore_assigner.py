# chore_assigner.py
import random
import datetime
from history_manager import load_chore_history, save_chore_history

def assign_daily_chores(daily_chores):
    history = load_chore_history()
    
    if history["feed_water"]["last_feed"] == "Kevin":
        am_feed, pm_feed = "John", "Kevin"
        am_water, pm_water = "Kevin", "John"
    else:
        am_feed, pm_feed = "Kevin", "John"
        am_water, pm_water = "John", "Kevin"

    daily_chores[0]["assigned_to"] = am_feed
    daily_chores[1]["assigned_to"] = pm_feed
    daily_chores[2]["assigned_to"] = am_water
    daily_chores[3]["assigned_to"] = pm_water

    history["feed_water"]["last_feed"] = pm_feed
    history["feed_water"]["last_water"] = pm_water
    save_chore_history(history)

def calculate_weights(chores):
    max_difficulty = max(chore['difficulty'] for chore in chores)
    return [max_difficulty - chore['difficulty'] + 1 for chore in chores]

def get_random_chore(user_name, chores, daily_chores, weekend_chores):
    assign_daily_chores(daily_chores)
    weights = calculate_weights(chores)
    chosen_chore = random.choices(chores, weights=weights, k=1)[0]
    print(f"{user_name}, your assigned chores are:")
    
    for daily in daily_chores:
        if daily.get("assigned_to") == user_name or "assigned_to" not in daily:
            print(f"- {daily['name']}")
    print(f"- {chosen_chore['name']}")

    today = datetime.datetime.now().weekday()
    if today in [5, 6]:
        for weekend_chore in weekend_chores:
            print(f"- {weekend_chore['name']}")
    return chosen_chore["name"]
