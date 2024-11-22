import json
import os
import datetime

history_file = "chore_history.json"

def default_history():
    """Returns the default structure for chore history."""
    return {
        "history": [],
        "dog_walk": {"last_person": None, "John": 0, "Kevin": 0},
        "feed_water": {"last_feed": "Kevin", "last_water": "John"}
    }

def load_chore_history():
    """Loads the chore history from a JSON file, initializing with defaults if the file is missing or corrupted."""
    if os.path.exists(history_file):
        try:
            with open(history_file, "r") as file:
                history = json.load(file)
            # Ensure necessary keys exist in loaded history
            history.setdefault("feed_water", {"last_feed": "Kevin", "last_water": "John"})
            history.setdefault("dog_walk", {"last_person": None, "John": 0, "Kevin": 0})
            return history
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading history file: {e}")
            # In case of error, initialize with default structure
    # Return default history if file doesn't exist or an error occurs
    return default_history()

def save_chore_history(history):
    """Saves the updated chore history to a JSON file."""
    try:
        with open(history_file, "w") as file:
            json.dump(history, file, indent=4)
    except IOError as e:
        print(f"Error saving history file: {e}")

def record_chore(user, chore_name, request_time, completion_time=None):
    """
    Records a chore for a user, including timestamps for request and optional completion.
    
    Args:
        user (str): The user's name who completed the chore.
        chore_name (str): Name of the chore.
        request_time (datetime): The timestamp when the chore was requested.
        completion_time (datetime, optional): The timestamp when the chore was completed.
    """
    history = load_chore_history()
    
    # Append new chore record to history
    history["history"].append({
        "user": user,
        "chore": chore_name,
        "request_time": request_time.strftime('%Y-%m-%d %H:%M:%S'),
        "completion_time": completion_time.strftime('%Y-%m-%d %H:%M:%S') if completion_time else None
    })
    
    # Save updated history
    save_chore_history(history)
