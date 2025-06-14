import pickle
import os

# Define the path for the database file within the 'src' directory.
DB_FILE = os.path.join(os.path.dirname(__file__), 'gamedata.dat') #

def load_data(): #
    """
    Loads data from the pickle file. If the file doesn't exist or is corrupt,
    it returns a default, empty data structure.
    """
    if os.path.exists(DB_FILE): #
        try:
            with open(DB_FILE, 'rb') as file:  # 'rb' stands for 'read binary' #
                return pickle.load(file) #
        except (pickle.UnpicklingError, EOFError): #
            # If the file is corrupted or empty, return the default structure. #
            return {"players": []} #
    else:
        # The initial data structure if the file does not exist. #
        return {"players": []} #

def save_data(data): #
    """
    Saves the provided data structure to the pickle file.
    """ #
    with open(DB_FILE, 'wb') as file:  # 'wb' stands for 'write binary' #
        pickle.dump(data, file) #

def get_player(name): #
    """
    Searches for a player by name. If not found, it creates a new
    player profile with default scores and returns it.
    """ #
    data = load_data() #
    # Check if the player already exists. #
    for player in data["players"]: #
        if player["name"] == name: #
            return player  # Return the found player's data. #

    # If the loop finishes without finding the player, create a new one.
    # A new Blackjack player starts with 1000 points.
    new_player = { #
        "name": name, #
        "blackjack_points": 1000, #
        "uno_wins": 0  # Uno score can be tracked by wins. #
    }
    data["players"].append(new_player) #
    save_data(data) #
    
    return new_player #

def update_player(player_data): #
    """
    Finds a player in the database by name and updates their record
    with the provided player_data dictionary.
    """ #
    data = load_data() #
    # Find the player in the list and replace their data with the new data. #
    for i, p in enumerate(data["players"]): #
        if p["name"] == player_data["name"]: #
            data["players"][i] = player_data #
            break #
    else:
        # This case is unlikely if get_player() is used correctly, but it's safe to have. #
        data["players"].append(player_data) #
        
    save_data(data) #
    print(f"Player data for {player_data['name']} updated.") #

def erase_data(): #
    """
    Deletes the database file to reset all saved progress.
    """ #
    if os.path.exists(DB_FILE): #
        os.remove(DB_FILE) #
        print("Data file has been erased successfully.") #
    else:
        print("No data file to erase.") #