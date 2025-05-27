from src.classes.deck import Deck, Card

class StandardCard(Card):
    def __init__(self, suit:str, value:str, frontSprite:str = '', backSprite:str = ''):
        super().__init__(frontSprite, backSprite)
        self.__suit = suit if suit in ('heart', 'diamond', 'club', 'spade') else 'undefined'
        self.__value = value if value in ('ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king') else 'undefined'

    def getSuit(self):
        return self.__suit
    def getValue(self):
        return  self.__value

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
                self.add(StandardCard(suit=suit, value=value))