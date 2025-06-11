from classes.deck import Deck, Card, Hand, Player

class StandardCard(Card):
    def __init__(self, suit:str, value:str, frontSprite:str = '', backSprite:str = ''):
        super().__init__(frontSprite, backSprite)
        self.__suit = suit if suit in ('heart', 'diamond', 'club', 'spade') else 'undefined'
        self.__value = value if value in ('ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king') else 'undefined'
        self.__frontSprite = frontSprite
        self.__backSprite = backSprite
        

    def getSuit(self):
        return self.__suit
    def getValue(self):
        return  self.__value
    def getfrontSprite(self):
        return self.__frontSprite
    def getbackSprite(self):
        return self.__backSprite
    

    def __str__(self):
        if self.getFace():
            return f'{self.__value} of {self.__suit}'
        else:
            return 'XXXXXXXXXX'

class StandardDeck(Deck):
    def createDeck(self):
        suits = ['heart', 'diamond', 'club', 'spade']
        values = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']
        for suit in suits:
            for value in values:
                self.add(StandardCard(suit=suit, value=value, frontSprite=f"{value}of{suit}.png", backSprite="cardBack_blue4.png"))

class StandardHand(Hand):
    def __init__(self):
        super().__init__()

    def sumValues(self):
        acc = 0
        aceAppeared = False
        for card in self.getCards():
            if card.getFace() and card.getValue != 'undefined':
                strValue = card.getValue()
                if strValue == 'jack' or strValue == 'queen' or strValue == 'king':
                    acc += 10
                elif strValue == 'ace':
                    acc += 1
                    aceAppeared = True
                else:
                    acc += int(strValue)
        if aceAppeared and acc < 12:
            acc += 10
        return acc
    
    #def print_Hand

class StardardPlayer(Player, StandardHand):
    def __init__(self, name, points = 1000):
        Player.__init__(self,name, points)
        StandardHand.__init__(self)