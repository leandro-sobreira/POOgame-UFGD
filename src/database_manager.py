import pickle
import os
from datetime import datetime # Import datetime to record the date

# Define the path for the database file within the 'src' directory.
DB_FILE = os.path.join(os.path.dirname(__file__), 'gamedata.dat')

def load_data():
    """
    Loads data from the file. If the file doesn't exist or is corrupt,
    it returns a default, empty win log structure.
    """
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'rb') as file:  # 'rb' stands for 'read binary'
                return pickle.load(file)
        except (pickle.UnpicklingError, EOFError):
            # If the file is corrupted or empty, return the default structure.
            return {"wins": []}
    else:
        # The initial data structure if the file does not exist.
        return {"wins": []}
    
def save_data(data):
    """
    Saves the provided data structure to the pickle file.
    """
    with open(DB_FILE, 'wb') as file:  # 'wb' stands for 'write binary'
        pickle.dump(data, file)

def log_win(player_name, final_score, game_name):
    """
    Logs a new win to the database
    """
    data = load_data()  # Load existing data

    new_win = {
        "player_name": player_name,
        "score": final_score,
        "game": game_name,
        "date": datetime.now().strftime("%d/%m/%y - %H:%M")
    }
    
    # Ensure the 'wins' key exists
    if "wins" not in data:
        data["wins"] = []

    data["wins"].append(new_win)
    save_data(data)
    print(f"Win for {player_name} won {final_score} points in {game_name}.")

def get_all_wins():
    """
    Retrieves all wins, sorted by score.
    """
    data = load_data()
    all_wins = data.get("wins", [])

    """	# Sort wins by score in descending order.
    all_wins.sort(key=lambda x: x["score"], reverse=True) """
    return all_wins

def erase_data(): 
    """
    Deletes the database file to reset all saved progress.
    """ 
    if os.path.exists(DB_FILE): 
        os.remove(DB_FILE) 
        print("Data file has been erased successfully.") 
    else:
        print("No data file to erase.") #