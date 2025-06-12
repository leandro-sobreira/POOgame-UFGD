from ..classes.standard import StandardDeck, StandardPlayer

class BlackjackGame:
    def __init__(self, player_data):
        self.player = StandardPlayer(player_data['name'], player_data['blackjack_points']) #
        self.table = StandardPlayer("Dealer") # The dealer can be represented as a player #
        self.gameDeck = StandardDeck() #
        self.bet_amount = 10 # Fixed bet for simplicity #
        
        self.state = "PLAYER_TURN" # Possible states: PLAYER_TURN, DEALER_TURN, ROUND_OVER #
        self.result = "" # e.g., "Player Wins!", "Bust!", "Push!" #

        self.start_round() #

    def start_round(self): #
        """Resets hands and deals initial cards for a new round.""" #
        self.state = "PLAYER_TURN" #
        self.result = "" #

        # Player pays the bet #
        self.player.remPoints(self.bet_amount) #

        # Clear hands and deck #
        self.player.clear() #
        self.table.clear() #
        self.gameDeck.clear() #
        self.gameDeck.createDeck() #
        self.gameDeck.shuffle() #

        # Deal initial cards #
        self.player.add(self.gameDeck.give()) #
        self.table.add(self.gameDeck.give()) # Dealer's first card (face up) #
        self.player.add(self.gameDeck.give()) #
        self.table.add(self.gameDeck.give(False)) # Dealer's second card (face down) #

        # Check for immediate Blackjack #
        if self.player.sumValues() == 21: #
            self.player_stand() #

    def player_hit(self): #
        """Player requests another card.""" #
        if self.state == "PLAYER_TURN": #
            self.player.add(self.gameDeck.give()) #
            if self.player.sumValues() > 21: #
                self.result = "Player Busts! Dealer Wins." #
                self.state = "ROUND_OVER" #
            elif self.player.sumValues() == 21: #
                self.player_stand() #

    def player_stand(self): #
        """Player finishes their turn, and the dealer plays.""" #
        if self.state == "PLAYER_TURN": #
            self.state = "DEALER_TURN" #
            self._dealer_play() #

    def _dealer_play(self): #
        """The dealer's automated turn logic.""" #
        self.table.flipAll(True) # Reveal the dealer's hole card #
        
        while self.table.sumValues() < 17: #
            self.table.add(self.gameDeck.give()) #
        
        self._determine_winner() #

    def _determine_winner(self): #
        """Compares hands and sets the final result and payout.""" #
        player_score = self.player.sumValues() #
        dealer_score = self.table.sumValues() #

        if player_score > 21: # This case is already handled but good for clarity #
            self.result = "Player Busts! Dealer Wins." #
        elif dealer_score > 21: #
            self.result = "Dealer Busts! Player Wins." #
            self.player.addPoints(self.bet_amount * 2) # Return bet + winnings #
        elif player_score > dealer_score: #
            self.result = "Player Wins!" #
            self.player.addPoints(self.bet_amount * 2) #
        elif dealer_score > player_score: #
            self.result = "Dealer Wins." #
        else: # Push #
            self.result = "Push (Draw)." #
            self.player.addPoints(self.bet_amount) # Return original bet #
        
        self.state = "ROUND_OVER" #

    def get_player_data(self): #
        """Returns the player's data in a dictionary format for saving.""" #
        return { #
            "name": self.player.getName(), #
            "blackjack_points": self.player.getPoints(), #
            # Include other game scores here if they were part of the original data #
        }