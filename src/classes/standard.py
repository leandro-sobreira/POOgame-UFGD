from .deck import Deck, Card, Hand, Player

class StandardCard(Card):
    def __init__(self, suit:str, value:str, frontSprite:str = 'joker', backSprite:str = 'joker'): #
        super().__init__(frontSprite, backSprite) #
        self.__suit = suit #
        self.__value = value #

    @property
    def suit(self): #
        return self.__suit
    
    @property
    def value(self): #
        return self.__value
    
    @suit.setter
    def suit(self, suit):
        self.__suit = suit
    
    @value.setter
    def value(self, value):
        self.__value = value    

    #SOBRECARGA DE OPERADOR
    def __str__(self): #
        if self.getFace(): #
            return f'{self.__value} of {self.__suit}' #
        else:
            return 'Face Down' #

class StandardDeck(Deck): #
    def __init__(self): #
        super().__init__() #

    def createDeck(self): #
        suits = ['heart', 'diamond', 'club', 'spade'] #
        values = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king'] #
        
        for suit in suits: #
            for value in values: #
                self.add(StandardCard(suit=suit, value=value, frontSprite=f'{value}_of_{suit}', backSprite='cardBack_red5')) #

class StandardHand(Hand): #
    def __init__(self): #
        super().__init__() #

    def sumValues(self): #
        total = 0 #
        aces_appears = False 
        for card in self.cards: #
            if card.faceUp: #
                value = card.value #
                if value in ('jack', 'queen', 'king'): #
                    total += 10 #
                elif value == 'ace': #
                    aces_appears = True #
                    total += 1
                else:
                    total += int(value) #
        
        # Adjust for aces if total is under 12 #
        while total < 12 and aces_appears:
            total += 10 #
        return total #

class StandardPlayer(Player, StandardHand):
    def __init__(self, name, points=1000):
        Player.__init__(self, name, points) 
        StandardHand.__init__(self) 
