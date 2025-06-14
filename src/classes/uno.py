import random

from .deck import Card, Deck, Hand, Player

class UnoCard(Card):
    def __init__(self, value:str, color:str = '', frontSprite:str = '', backSprite:str = ''):
        super().__init__(frontSprite, backSprite)
        self.__value = value
        self.__color = color

    @property
    def color(self):
        return self.__color
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        self.__value = value

    @color.setter
    def color(self, color:str):
        if color in ('red', 'yellow', 'green', 'blue', '') and self.__value in ('wild', '+4'):
            self.__color = color
            if color == '':
                self._Card__sprite = f'{self.__value}'
            else:
                self._Card__sprite = f'{color}_{self.__value}'
            #TODO:Ver se essa forma está certa ou é melhor fazer um setSprite()
    
    def match(self, card):
        if self.__color == '' or card.color == '':
            return True
        
        return self.__color == card.color or self.__value == card.value

    #SOBRECARGA DE OPERADOR
    def __str__(self):
        if self._Card__faceUp:
            return f'{self.__color} {self.__value}' if self.__color else f'{self.__value}'
        else:
            return 'Face Down'

class UnoDeck(Deck):
    def __init__(self):
        super().__init__()

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
        for card in self.cards:
            if card.value in ('+2', 'block', 'reverse'):
                total += 20
            elif card.value in ('+4', 'wild'):
                total += 50
            else:
                total += int(card.value)
        return total

    def sort(self):
        self.cards.sort(key=lambda card: (card.color, card.value))

class UnoPlayer(Player, UnoHand):
    def __init__(self, name, points = 0):
        Player.__init__(self, name, points)
        UnoHand.__init__(self)

class UnoPlayers:
    def __init__(self, playerName):
        playersNames = [playerName, 'Bot1', 'Bot2', 'Bot3']
        self.__players = [UnoPlayer(name) for name in playersNames]
        self.__turn = 0
        self.__rotation = 1

    @property
    def turn(self):
        return self.__turn
    
    @property
    def rotation(self):
        return self.__rotation

    @property
    def players(self):
        return self.__players

    @turn.setter
    def turn(self, turn):
        self.__turn = turn
    
    @rotation.setter
    def rotation(self, rotation):
        self.__rotation = rotation
    
    @players.setter
    def players(self, players):
        self.__players = players

    def flipRotation(self):
        self.__rotation *= -1    
    
    def setNextTurn(self):
        self.__turn = (self.__turn + self.__rotation) % len(self.__players)
    
    def getCurrentPlayer(self):
        return self.__players[self.__turn]
    
    def getNextPlayer(self):
        return self.__players[self.getNextTurn()]
    
    def getNextTurn(self):
        return (self.__turn + self.__rotation) % len(self.__players)
    
    def getHumanPlayer(self):
        return self.__players[0]
    
    #SOBRECARGA DE OPERADOR
    def __getitem__(self, index):
        return self.__players[index]