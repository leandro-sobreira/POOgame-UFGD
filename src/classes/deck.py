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

    def Flip(self):
        self.__face = self.__face == False
        if self.__face:
            self.__sprite = self.__frontSprite
        else:
            self.__sprite = self.__backSprite


class Deck:
    def __init__(self):
        self.__numCards:int = 0
        self.__deck = []

    def getNumCards(self):
        return self.__numCards

    def add(self, card):
        self.__deck.append(card)
        self.__numCards += 1

    def __add__(self, card):
        self.add(card)

    def discard(self):
        if self.__numCards > 0:
            self.__deck.pop()
            self.__numCards -= 1

    def give(self, flip:bool = True):
        if self.__numCards > 0:
            card = self.__deck[self.__numCards -1]
            if flip:
                card.Flip()
            self.discard()
            return card
        return None

    def suffle(self):
        random.shuffle(self.__deck)

    def flipAll(self, stat): #True to front up
        for card in self.__deck:
            if card.getFace() != stat:
                card.Flip()

    def __getitem__(self, item):
        return self.__deck[item]