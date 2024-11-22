import datetime
import json
from email_utils import send_at_home_email, send_electronics_email, send_email
from history_manager import record_chore
from chore_assigner import get_random_chore

# Load chores from JSON file
def load_chores():
    """Loads chores data from chores.json file with error handling."""
    try:
        with open("chores.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading chores: {e}")
        return {"chores": [], "daily_chores": [], "weekend_chores": []}

def load_chore_history(file_name):
    """Loads chore history data from a specified JSON file."""
    try:
        with open(file_name, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading chore history: {e}")
        return {}  # Return an empty dictionary if loading fails

def save_chore_history(file_name, data):
    """Saves chore history data to a specified JSON file."""
    try:
        with open(file_name, "w") as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        print(f"Error saving chore history: {e}")

chores_data = load_chores()
chores = chores_data["chores"]
daily_chores = chores_data["daily_chores"]
weekend_chores = chores_data["weekend_chores"]

# Tracking user data for electronics time and restrictions
user_data = {
    "John": {"chore_request_time": None, "chore_completion_time": None, "extra_chore_requested": None, "electronics_start_time": None, "restricted": False},
    "Kevin": {"chore_request_time": None, "chore_completion_time": None, "extra_chore_requested": None, "electronics_start_time": None, "restricted": False}
}

# Dog-walking turn tracking
dog_walking_data = {"John": 0, "Kevin": 0}

def whose_turn_to_walk():
    """Determines whose turn it is to take the dog out based on ratio."""
    if dog_walking_data["John"] <= dog_walking_data["Kevin"]:
        return "John"
    else:
        return "Kevin"

def mark_dog_walked(user_name):
    """Marks the dog as walked by the user and adjusts the ratio."""
    if user_name not in dog_walking_data:
        dog_walking_data[user_name] = 0  # Initialize if missing
    dog_walking_data[user_name] += 1
    print(f"{user_name} has walked the dog. Current ratio: John - {dog_walking_data.get('John', 0)}, Kevin - {dog_walking_data.get('Kevin', 0)}")
    save_chore_history("dog_walking_data.json", dog_walking_data)

def mark_chores_complete(user_name):
    """Marks chores as completed for the user and records completion time, sends completion email."""
    user_data[user_name]["chore_completion_time"] = datetime.datetime.now()
    record_chore(user_name, "All chores", user_data[user_name]["chore_request_time"], user_data[user_name]["chore_completion_time"])
    completion_time = user_data[user_name]["chore_completion_time"].strftime('%Y-%m-%d %H:%M:%S')
    subject = f"All Chores Completed by {user_name}"
    body = f"All chores for {user_name} have been marked as complete as of {completion_time}."
    send_email(subject, body)
    print(f"All chores marked as complete for {user_name}.\n")

def check_grade_and_manage_electronics(user_name):
    """Checks the user's grade to determine electronics time restrictions."""
    valid_grades = ["A", "B", "C", "D", "F"]
    grade = input(f"{user_name}, enter your lowest grade (A, B, C, D, or F): ").upper()
    while grade not in valid_grades:
        print("Invalid grade entered. Please enter A, B, C, D, or F.")
        grade = input(f"{user_name}, enter your lowest grade (A, B, C, D, or F): ").upper()
    
    if grade in ["A", "B", "C"]:
        print(f"{user_name} has no electronics time restrictions.")
        user_data[user_name]["restricted"] = False
    else:  # For grades "D" or "F"
        print(f"{user_name}'s electronics time is restricted to 1 hour due to grade below C.")
        user_data[user_name]["restricted"] = True
        electronics_time(user_name)

def electronics_time(user_name):
    """Manages electronics start and end times based on restriction status."""
    current_time = datetime.datetime.now()
    if user_data[user_name]["electronics_start_time"] is None:
        user_data[user_name]["electronics_start_time"] = current_time
        print(f"{user_name} started electronics time at {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
        if user_data[user_name]["restricted"]:
            end_time = current_time + datetime.timedelta(hours=1)
            print(f"{user_name}'s restricted electronics time will end at {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        send_electronics_email(user_name, current_time, "start", user_data[user_name]["restricted"])
    else:
        end_restricted_electronics_time(user_name)

def end_restricted_electronics_time(user_name):
    """Ends restricted electronics time and logs the completion."""
    end_time = datetime.datetime.now()
    start_time = user_data[user_name]["electronics_start_time"]
    duration = end_time - start_time
    user_data[user_name]["electronics_start_time"] = None
    exceeded = user_data[user_name]["restricted"] and duration > datetime.timedelta(hours=1)
    send_electronics_email(user_name, end_time, "end", user_data[user_name]["restricted"], duration, exceeded)
    print(f"{user_name} ended electronics time at {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

def menu():
    """Displays and processes the chore program menu."""
    while True:
        print("\nChore Program Menu:")
        print("1. Get a chore")
        print("2. Mark all chores as complete")
        print("3. Check Grade and Manage Electronics Time")
        print("4. Mark as At Home")
        print("5. See whose turn it is to walk the dog")
        print("6. Mark dog as walked")
        
        # Show option to end electronics time only if restricted
        if any(user["restricted"] and user["electronics_start_time"] is not None for user in user_data.values()):
            print("7. End Electronics Time")
            print("8. Exit")
            exit_choice = "8"
        else:
            print("7. Exit")
            exit_choice = "7"

        choice = input("Choose an option: ")
        user_choice = input("Press 1 if you are John, press 2 if you are Kevin: ")
        user_name = "John" if user_choice == "1" else "Kevin" if user_choice == "2" else None

        if user_name:
            if choice == "1":
                chosen_chore = get_random_chore(user_name, chores, daily_chores, weekend_chores)
                user_data[user_name]["chore_request_time"] = datetime.datetime.now()
                record_chore(user_name, chosen_chore, user_data[user_name]["chore_request_time"])
            elif choice == "2":
                mark_chores_complete(user_name)
            elif choice == "3":
                check_grade_and_manage_electronics(user_name)
            elif choice == "4":
                send_at_home_email(user_name)
            elif choice == "5":
                turn = whose_turn_to_walk()
                print(f"It's {turn}'s turn to walk the dog.")
            elif choice == "6":
                mark_dog_walked(user_name)
            elif choice == "7" and exit_choice == "8":  # End Electronics Time
                end_restricted_electronics_time(user_name)
            elif choice == exit_choice:  # Exit program
                print("Goodbye!")
                break
            else:
                print("Invalid choice, please try again.\n")
        else:
            print("Invalid user choice. Please try again.\n")

if __name__ == "__main__":
    # Initialize dog walking data from file if available
    try:
        dog_walking_data = load_chore_history("dog_walking_data.json")
    except Exception as e:
        print(f"Error loading dog walking data: {e}")
        dog_walking_data = {"John": 0, "Kevin": 0}
        save_chore_history("dog_walking_data.json", dog_walking_data)
    menu()
