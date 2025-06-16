import pickle
import os
from datetime import datetime # Import datetime to record the date

# Define the path for the database file within the 'src' directory.
DB_FILE = os.path.join(os.path.dirname(__file__), 'gamedata.dat')

def load_data():
    """
    Carrega os dados de um arquivo de dados. Se o arquivo não existir ou
    tiver corrompido, retornar por padrão, um arquivo de wins vazio

    Returns:
        dict {key: list[int]} : dict representando o arquivo de banco de dados de wins
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
    Salva os dados obtidos e estruturados em um arquivo pickle

    Argumentos:
        data (dict {key: list[int]}) : Dados estruturados a serem salvos e atualizados no banco 
                                       de dados não estruturado
    """
    with open(DB_FILE, 'wb') as file:  # 'wb' stands for 'write binary'
        pickle.dump(data, file)

def log_win(player_name, final_score, game_name):
    """
    Realiza o log da vitória obtida 

    Argumentos:
        player_name (str) : string representando o nome do jogador a ser registrado
        final_score (int) : string representando a pontuação final do jogador a ser registrada
        game_name (str) : string representando o nome do jogo que foi jogado a ser registrado
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
    Obtém todas as vitórias registradas no banco de dados

    Returns:
        list[int] : lista de todas as vitórias obtidas com as determinadas pontuações   
    """
    data = load_data()
    all_wins = data.get("wins", [])

    """	# Sort wins by score in descending order.
    all_wins.sort(key=lambda x: x["score"], reverse=True) """

    return all_wins

def erase_data(): 
    """
    Deleta o arquivo de database e reseta todas as pontuações obtidas e registradas no banco de dados
    """ 
    if os.path.exists(DB_FILE): 
        os.remove(DB_FILE) 
        print("Data file has been erased successfully.") 
    else:
        print("No data file to erase.") #