import random
from abc import ABC, abstractmethod

#implementar o deck de descarte
class Card(ABC):
    def __init__(self, frontSprite:str= '', backSprite:str= ''):
        self.__frontSprite = frontSprite
        self.__backSprite = backSprite
        self.__sprite = frontSprite
        self.__faceUP:bool = False

    def getFrontSprite(self):
        return self.__frontSprite
    def getBackSprite(self):
        return self.__backSprite
    def getSprite(self):
        return self.__sprite
    def getFace(self):
        return self.__face

    def flip(self):
        self.__face = self.__faceUP == False
        if self.__face:
            self.__sprite = self.__frontSprite
        else:
            self.__sprite = self.__backSprite


class Deck(ABC):
    def __init__(self):
        self.__numCards:int = 0
        self.__cards = []

    def getNumCards(self):
        return self.__numCards

    def add(self, card):
        self.__cards.append(card)
        self.__numCards += 1

    def __add__(self, card):
        self.add(card)

    def discard(self):
        if self.__numCards > 0:
            self.__cards.pop()
            self.__numCards -= 1

    def give(self, flip:bool = True):
        if self.__numCards > 0:
            card = self.__cards[self.__numCards -1]
            if flip:
                card.Flip()
            self.discard()
            return card
        return None

    def suffle(self):
        random.shuffle(self.__cards)

    @abstractmethod
    def createDeck(self):
        pass

class Hand(ABC):
    def __init__(self):
        self.__cards = []

    def add(self, card):
        self.__cards.append(card)

    def __iadd__(self, card):
        self.add(card)

    def __getitem__(self, item):
        return self.__cards[item]

    def discard(self, item):
        self.__cards.remove(item)

    def give(self, item):
        card = self[item]
        self.__cards.remove(item)
        return card

    def flipAll(self, stat): #True to front up
        for card in self.__cards:
            if card.getFace() != stat:
                card.flip()


class Player(ABC):
    def __init__(self, name: str, points: int):
        super().__init__()
        self.__name = name
        self.__points = points

    def getName(self):
        return self.__name

    def getPoints(self):
        return self.__name

    def addPoints(self, amount: int):
        self.__points += amount

    def remPoints(self, amount: int):
        self.__points -= amount

