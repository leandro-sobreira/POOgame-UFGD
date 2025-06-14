from ..classes.standard import StandardDeck, StandardPlayer

class BlackjackGame:
    def __init__(self, player_data):
        self.__player = StandardPlayer(player_data['name'], player_data['blackjack_points']) #
        self.__table = StandardPlayer("Dealer") # The dealer can be represented as a player #
        self.__gameDeck = StandardDeck() #
        #self.bet_amount = 10 # Fixed bet for simplicity # TODO
        # Chame a tela de input de aposta aqui:
        #bet_screen = 0 #bet_screen = amount
        # Em vez de usar bet_screen.loop()
        self.__betAmount = 0

        
        self.__state = "BET" # Possible states: PLAYER_TURN, DEALER_TURN, ROUND_OVER #
        self.__result = "" # e.g., "Player Wins!", "Bust!", "Push!" #

        self.setBetAmount()

    @property
    def player(self):
        return self.__player
    
    @property
    def table(self):
        return self.__table
    
    @property
    def gameDeck(self):
        return self.__gameDeck
    
    @property
    def betAmount(self):
        return self.__betAmount
    
    @property
    def state(self):
        return self.__state
    
    @property
    def result(self):
        return self.__result
    
    @player.setter
    def player(self, player):
        self.__player = player
    
    @table.setter
    def player(self, table):
        self.__table = table
    
    @gameDeck.setter
    def gameDeck(self, gameDeck):
        self.__gameDeck = gameDeck
    
    @betAmount.setter
    def betAmount(self, betAmount):
        self.__betAmount = betAmount
    
    @state.setter
    def state(self, state):
        self.__state = state
    
    @result.setter
    def result(self, result):
        self.__result = result

    def setBetAmount(self):
        if self.__betAmount < 10 or self.__betAmount > self.__player.points:
            self.__state = "BET"
        else:
            self.start_round()

    def start_round(self): #
        """Resets hands and deals initial cards for a new round.""" #
        self.__state = "PLAYER_TURN" #
        self.__result = "" #

        # Player pays the bet #
        self.__player.remPoints(self.__betAmount) #

        # Clear hands and deck #
        self.__player.clear() #
        self.__table.clear() #
        self.__gameDeck.clear() #
        self.__gameDeck.createDeck() #
        self.__gameDeck.shuffle() #

        # Deal initial cards #
        self.__player.add(self.__gameDeck.give()) #
        self.__table.add(self.__gameDeck.give()) # Dealer's first card (face up) #
        self.__player.add(self.__gameDeck.give()) #
        self.__table.add(self.__gameDeck.give(False)) # Dealer's second card (face down) #

        # Check for immediate Blackjack #
        if self.__player.sumValues() == 21: #
            self.player_stand() #

    def player_hit(self): #
        """Player requests another card.""" #
        if self.__state == "PLAYER_TURN": #
            self.__player.add(self.__gameDeck.give()) #
            if self.__player.sumValues() > 21: #
                self.__result = "Player Busts! Dealer Wins." #
                self.__state = "ROUND_OVER" #
            elif self.__player.sumValues() == 21: #
                self.player_stand() #

    def player_stand(self): #
        """Player finishes their turn, and the dealer plays.""" #
        if self.__state == "PLAYER_TURN": #
            self.__state = "DEALER_TURN" #
            self._dealer_play() #
            #self.table.flipAll(True)

    def _dealer_play(self): #
        """The dealer's automated turn logic.""" #
        self.__table.flipAll(True) # Reveal the dealer's hole card #
        while self.__table.sumValues() and self.__table.sumValues() < 17:
            self.__table.add(self.__gameDeck.give()) #
        self._determine_winner() #

    """def _dealer_buy_loop(self):
            if self.table.sumValues() < 50:
                self.table.add(self.gameDeck.give()) #
            else:
                self._determine_winner() #"""
            

    def _determine_winner(self): #
        """Compares hands and sets the final result and payout.""" #
        player_score = self.__player.sumValues() #
        dealer_score = self.__table.sumValues() #

        if player_score > 21: # This case is already handled but good for clarity #
            self.__result = "Player Busts! Dealer Wins." #
        elif dealer_score > 21: #
            self.__result = "Dealer Busts! Player Wins." #
            self.__player.addPoints(self.__bet_amount * 2) # Return bet + winnings #
        elif player_score > dealer_score: #
            self.__result = "Player Wins!" #
            self.__player.addPoints(self.__bet_amount * 2) #
        elif dealer_score > player_score: #
            self.__result = "Dealer Wins." #
        else: # Push #
            self.__result = "Push (Draw)." #
            self.__player.addPoints(self.__bet_amount) # Return original bet #
        
        self.__bet_amount = 0
        self.__state = "ROUND_OVER" #

    def get_player_data(self): #
        """Returns the player's data in a dictionary format for saving.""" #
        return { #
            "name": self.__player.name, #
            "blackjack_points": self.__player.points, #
            # Include other game scores here if they were part of the original data #
        }