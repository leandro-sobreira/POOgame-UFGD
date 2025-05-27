from src.classes.standard import Deck

class Player(Deck):
    def __init__(self, name:str, points:int):
        super().__init__()
        self.__name = name
        self.__points = points

    def getName(self):
        return self.__name
    def getPoints(self):
        return self.__name

    def addPoints(self, amount:int):
        self.__points += amount
    def remPoints(self, amount:int):
        self.__points -= amount