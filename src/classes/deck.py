import random
from abc import ABC, abstractmethod

class Card(ABC):
    def __init__(self, frontSprite:str= '', backSprite:str= ''):
        self.__frontSprite = frontSprite
        self.__backSprite = backSprite
        self.__sprite = frontSprite
        self.__faceUp:bool = False

    def getFrontSprite(self):
        return self.__frontSprite
    def getBackSprite(self):
        return self.__backSprite
    def getSprite(self):
        return self.__sprite
    def getFace(self):
        return self.__faceUp

    def flip(self):
        self.__faceUp = self.__faceUp == False
        if self.__faceUp:
            self.__sprite = self.__frontSprite
        else:
            self.__sprite = self.__backSprite


class Deck(ABC):
    def __init__(self):
        self.__cards = []

    def isEmpty(self):
        return self.__cards == []

    def add(self, card):
        self.__cards.append(card)

    def __iadd__(self, card):
        self.add(card)

    def discard(self):
        self.__cards.pop()

    def clear(self):
        self.__cards.clear()

    def size(self):
        return len(self.__cards)

    def give(self, flip:bool = True):
        if not self.isEmpty() :
            card = self.__cards[self.size() -1]
            if flip:
                card.flip()
            self.discard()
            return card
        return None

    def shuffle(self):
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

    def getCards(self):
        return self.__cards

    def size(self):
        return len(self.__cards)

    def give(self, item):
        card = self[item]
        self.__cards.remove(item)
        return card

    def flipAll(self, stat): #True to front up
        for card in self.__cards:
            if card.getFace() != stat:
                card.flip()


class Player(ABC):
    def __init__(self, name: str, points: int = 0):
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

