import random
import os
from abc import ABC, abstractmethod

import setup as st

class Card(ABC):
    def __init__(self, frontSprite:str= '', backSprite:str= ''):
        
        self.__frontSprite = frontSprite
        self.__backSprite = backSprite
        self.__sprite = backSprite
        self.__faceUp:bool = False

    @property
    def frontSprite(self):
        return self.__frontSprite
    
    @property
    def backSprite(self):
        return self.__backSprite
    
    @property
    def sprite(self):
        return self.__sprite
    
    @property
    def faceUp(self):
        return self.__faceUp
    
    @frontSprite.setter
    def frontSprite(self, frontSprite):
        self.__frontSprite = frontSprite

    @backSprite.setter
    def backSprite(self, backSprite):
        self.__backSprite = backSprite
    
    @sprite.setter
    def sprite(self, sprite):
        self.__sprite = sprite
    
    @faceUp.setter    
    def faceUp(self, faceUp:bool):
        self.__faceUp = faceUp

        if faceUp:
            self.__sprite = self.__frontSprite
        else:
            self.__sprite = self.__backSprite

    def flip(self):
        self.__faceUp = self.__faceUp == False
        if self.__faceUp:
            self.__sprite = self.__frontSprite
        else:
            self.__sprite = self.__backSprite


class Deck(ABC):
    def __init__(self):
        self.__cards = []

    @property
    def cards(self):
        return self.__cards
    
    @cards.setter
    def cards(self, cards):
        self.__cards = cards

    def topCard(self):
        return self.__cards[-1]

    def isEmpty(self):
        return not self.__cards

    def add(self, card):
        self.__cards.append(card)

    #SOBRECARGA DE OPERADOR
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
            card = self.__cards[-1]
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

    def isEmpty(self):
        return not self.__cards

    def add(self, card):
        self.__cards.append(card)
    
    #SOBRECARGA
    def __iadd__(self, card):
        self.add(card)

    def __getitem__(self, item):
        return self.__cards[item]

    def getCards(self):
        return self.__cards

    def size(self):
        return len(self.__cards)

    def give(self, card):
        self.__cards.remove(card)

        return card
    
    def clear(self):
        self.__cards.clear()

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
        return self.__points

    def addPoints(self, amount: int):
        self.__points += amount

    #SOBRECARGA

    def __iadd__(self, amount: int):
        self.addPoints(amount)

    def remPoints(self, amount: int):
        #Adicionar tratamento de erro
        self.__points -= amount

    #SOBRECARGA

    def __isub__(self, amount: int):
        self.remPoints(amount)

    def givePoints(self, amount:int):
        self.remPoints(amount)
        
        return amount