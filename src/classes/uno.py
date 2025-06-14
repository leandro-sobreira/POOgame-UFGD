from .deck import Card, Deck, Hand, Player
import random

# CORRECTED: Removed the first, incomplete definition of UnoCard
class UnoCard(Card):
    def __init__(self, value:str, color:str = '', frontSprite:str = '', backSprite:str = ''):
        super().__init__(frontSprite, backSprite)
        self.__value = value
        self.__color = color

    def getColor(self):
        return self.__color
        
    def getValue(self):
        return self.__value
        
    def setColor(self, color:str):
        if color in ('red', 'yellow', 'green', 'blue', '') and self.__value in ('wild', '+4'):
            self.__color = color
            if color == '':
                self._Card__sprite = f'{self.__value}'
            else:
                self._Card__sprite = f'{color}_{self.__value}'
            #TODO:Ver se essa forma está certa ou é melhor fazer um setSprite()
    
    def match(self, card):
        if self.__color == '' or card.getColor() == '':
            return True
        return self.__color == card.getColor() or self.__value == card.getValue()

    def __str__(self):
        if self.getFace():
            return f'{self.__color} {self.__value}' if self.__color else f'{self.__value}'
        else:
            return 'Face Down'

# ... (rest of the file is the same)
class UnoDeck(Deck):
    def createDeck(self):
        colors = ['red', 'yellow', 'green', 'blue']
        values = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+2', 'block', 'reverse']
        for color in colors:
            for value in values:
                self.add(UnoCard(value=value, color=color, frontSprite=f'{color}_{value}', backSprite='back'))
                if value != '0':
                    self.add(UnoCard(value=value, color=color, frontSprite=f'{color}_{value}', backSprite='back'))
        for i in range(4):
            self.add(UnoCard(value='wild', frontSprite='wild', backSprite='back'))
        for i in range(4):
            self.add(UnoCard(value='+4', frontSprite='+4', backSprite='back'))

class UnoHand(Hand):
    def __init__(self):
        super().__init__()

    def sumValues(self):
        total = 0
        for card in self.getCards():
            if card.getValue() in ('+2', 'block', 'reverse'):
                total += 20
            elif card.getValue() in ('+4', 'wild'):
                total += 50
            else:
                total += int(card.getValue())
        return total

    def sort(self):
        self.getCards().sort(key=lambda card: (card.getColor(), card.getValue()))

class UnoPlayer(Player, UnoHand):
    def __init__(self, name, points = 0):
        super().__init__(name, points)

class UnoPlayers:
    def __init__(self, playerName):
        playersNames = [playerName, 'Bot1', 'Bot2', 'Bot3']
        self.__players = [UnoPlayer(name) for name in playersNames]
        self.__turn = 0
        self.__rotation = 1

    def getTurn(self):
        return self.__turn

    def clear(self):
        self.__turn = 0
        self.__rotation = 1
        for player in self.__players:
            player.clear()
    
    def getNextTurn(self):
        return (self.__turn + self.__rotation) % len(self.__players)
    
    def setNextTurn(self):
        self.__turn = (self.__turn + self.__rotation) % len(self.__players)
    
    def getRotation(self):
        return self.__rotation

    def flipRotation(self):
        self.__rotation *= -1

    def getPlayers(self):
        return self.__players
    
    def getCurrentPlayer(self):
        return self.__players[self.__turn]
    
    def getNextPlayer(self):
        return self.__players[self.getNextTurn()]
    
    def getHumanPlayer(self):
        return self.__players[0]
    
    def __getitem__(self, index):
        return self.__players[index]