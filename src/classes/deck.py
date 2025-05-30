import random
from abc import ABC, abstractmethod

class Card(ABC):
    def __init__(self, frontSprite:str= '', backSprite:str= ''):
        self.__frontSprite = frontSprite
        self.__backSprite = backSprite
        self.__sprite = frontSprite
        self.__face:bool = False #Is front face Up

    def getFrontSprite(self):
        return self.__frontSprite
    def getBackSprite(self):
        return self.__backSprite
    def getSprite(self):
        return self.__sprite
    def getFace(self):
        return self.__face

    def flip(self):
        self.__face = self.__face == False
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
    def getCards(self):
        return self.__cards

    def add(self, card):
        self.__cards.append(card)
        self.__numCards += 1

    def discard(self):
        if self.__numCards > 0:
            self.__cards.pop()
            self.__numCards -= 1

    def give(self):
        if self.__numCards > 0:
            card = self.__cards[self.__numCards -1]
            card.flip()
            self.discard()
            return card
        return None

    def suffle(self):
        random.shuffle(self.__cards)