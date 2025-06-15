import os
import sys
import random

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from database_manager import log_win
except ImportError:
    sys.exit(1)

def inject_scores():
    player_names = ["Alice", "Bob", "Charlie", "Diana", "Eve"]

    for i in range(10):
        player = random.choice(player_names) + str(random.randint(1, 9))
        score = random.randint(100, 1000)* 10
        log_win(player_name=player, final_score=score, game_name="Blackjack")
    
    for i in range(10):
        player = random.choice(player_names) + str(random.randint(1, 9))
        score = random.randint(50, 600)
        log_win(player_name=player, final_score=score, game_name="Uno")

if __name__ == "__main__":
    inject_scores()

    

