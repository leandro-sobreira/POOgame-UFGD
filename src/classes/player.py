from src.classes.standard import Deck

class Hand(Deck):

    def flipAll(self, stat): #True to front up
        for card in self.__cards:
            if card.getFace() != stat:
                card.flip()

    def __iadd__(self, card):
        self.add(card)

    def __getitem__(self, item):
        return self.getCards()[item]

class Player:
    def __init__(self, name:str, points:int, handType):
        super().__init__()
        self.__name = name
        self.__points = points
        self._hand = handType

    def getName(self):
        return self.__name
    def getPoints(self):
        return self.__name
    def getHand(self):
        return self._hand

    def addPoints(self, amount:int):
        self.__points += amount
    def remPoints(self, amount:int):
        self.__points -= amount

    def __getitem__(self, item):
        return self.__hand[item]