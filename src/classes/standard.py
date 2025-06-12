from classes.deck import Deck, Card, Hand, Player

class StandardCard(Card):
    def __init__(self, suit:str, value:str):
        super().__init__()
        self.__suit = suit
        self.__value = value

    def getSuit(self):
        return self.__suit
    
    def getValue(self):
        return self.__value

    def get_image_path(self):
        """Maps card data to its image filename (e.g., cardSpadesK)."""
        suit_map = {'spade': 'Spades', 'heart': 'Hearts', 'club': 'Clubs', 'diamond': 'Diamonds'}
        value_map = {'ace': 'A', 'jack': 'J', 'queen': 'Q', 'king': 'K'}
        
        value_str = value_map.get(self.__value, self.__value)
        suit_str = suit_map.get(self.__suit)
        
        return f"card{suit_str}{value_str}"

    def __str__(self):
        if self.getFace():
            return f'{self.__value} of {self.__suit}'
        else:
            return 'Face Down'

class StandardDeck(Deck):
    def createDeck(self):
        suits = ['heart', 'diamond', 'club', 'spade']
        values = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']
        for suit in suits:
            for value in values:
                self.add(StandardCard(suit=suit, value=value))

class StandardHand(Hand):
    def __init__(self):
        super().__init__()

    def sumValues(self):
        total = 0
        num_aces = 0
        for card in self.getCards():
            if card.getFace():
                value = card.getValue()
                if value in ('jack', 'queen', 'king'):
                    total += 10
                elif value == 'ace':
                    num_aces += 1
                    total += 11 # Assume ace is 11 initially
                else:
                    total += int(value)
        
        # Adjust for aces if total is over 21
        while total > 21 and num_aces > 0:
            total -= 10
            num_aces -= 1
        return total

class StardardPlayer(Player, StandardHand):
    def __init__(self, name, points=1000):
        Player.__init__(self, name, points)
        StandardHand.__init__(self) # CORRECTED: Called the superclass initializer