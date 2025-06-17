import pickle
import os
from datetime import datetime
from typing import List

# The path to the data file remains defined here.
DB_FILE = os.path.join(os.path.dirname(__file__), 'gamedata.dat')

class ScoreEntry:
    """
    Represents a single win record, encapsulating the data from a
    completed game. This class replaces the use of dictionaries for score data.
    """
    def __init__(self, player_name: str, score: int, game_name: str, timestamp: datetime = None):
        """
        Initializes a new ScoreEntry object.
        """
        self.__player_name = player_name
        self.__score = score
        self.__game_name = game_name
        self.__timestamp = timestamp or datetime.now()

    def __repr__(self) -> str:
        """Provides a clear textual representation of the object, useful for debugging."""
        return (f"ScoreEntry(player='{self.__player_name}', score={self.__score}, "
                f"game='{self.__game_name}', date='{self.__timestamp.strftime('%d/%m/%y - %H:%M')}')")

class ScoreRepository:
    """
    Manages the loading and saving of score records, abstracting the
    file persistence logic. This class replaces the previous procedural functions.
    """
    def __init__(self, file_path: str = DB_FILE):
        self._file_path = file_path
        self._scores: List[ScoreEntry] = self._load_scores()

    def _load_scores(self) -> List[ScoreEntry]:
        """
        Loads score records from the file. If the data is in an old format
        (list of dicts, or dict containing a 'wins' list), it migrates
        it to a list of ScoreEntry objects.
        """
        if not os.path.exists(self._file_path):
            return []

        try:
            with open(self._file_path, 'rb') as f:
                data = pickle.load(f)

            # --- ROBUST DATA MIGRATION LOGIC ---
            
            list_to_process = []
            # 1. Handle original format: {'wins': [...]}
            if isinstance(data, dict) and 'wins' in data:
                list_to_process = data['wins']
            # 2. Handle list format (could be old list of dicts or new list of objects)
            elif isinstance(data, list):
                list_to_process = data
            else:
                # Unrecognized format, start fresh
                return []
            
            if not list_to_process:
                return []

            # 3. Check if migration is needed (is the first item a dict?)
            if isinstance(list_to_process[0], dict):
                migrated_scores = []
                for old_entry in list_to_process:
                    try:
                        timestamp = datetime.strptime(old_entry.get('date'), "%d/%m/%y - %H:%M")
                    except (ValueError, TypeError, KeyError):
                        timestamp = datetime.now()
                    
                    migrated_scores.append(ScoreEntry(
                        player_name=old_entry.get('player_name', 'Unknown'),
                        score=int(old_entry.get('score', 0)),
                        game_name=old_entry.get('game', 'Unknown'),
                        timestamp=timestamp
                    ))
                
                self._scores = migrated_scores
                self._save_scores()  # Overwrite the old file with the new format
                return self._scores

            # 4. If the first item is a ScoreEntry, assume the data is already in the correct format
            if isinstance(list_to_process[0], ScoreEntry):
                return list_to_process

        except (pickle.UnpicklingError, EOFError, IndexError, AttributeError):
            # Return an empty list if the file is corrupt, empty, or fails inspection
            return []

        # Fallback for any other unexpected data structure
        return []

    def _save_scores(self):
        """
        Saves the current list of ScoreEntry objects to the file.
        """
        with open(self._file_path, 'wb') as f:
            pickle.dump(self._scores, f)

    def add_score(self, player_name: str, final_score: int, game_name: str):
        """
        Creates a new ScoreEntry, adds it to the list, and saves.
        """
        entry = ScoreEntry(player_name, final_score, game_name)
        self._scores.append(entry)
        self._save_scores()
        print(f"Win for {player_name} with a score of {final_score} in {game_name} has been logged.")

    def get_all_scores(self) -> List[ScoreEntry]:
        """
        Returns all score records, sorted from highest to lowest score.
        """
        return sorted(self._scores, key=lambda entry: entry.score, reverse=True)

    def clear_all(self):
        """
        Deletes all score records and removes the data file.
        """
        self._scores = []
        if os.path.exists(self._file_path):
            os.remove(self._file_path)
            print("Data file has been erased successfully.")
        else:
            print("No data file to erase.")