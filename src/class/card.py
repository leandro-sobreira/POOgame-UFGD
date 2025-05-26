class Card:
    def __init__(self, suit:str, value:str, fpng:str, bpng:str):
        self.__suit = suit if suit in ('heart', 'diamond', 'club', 'spade') else 'undefined'
        self.__value = value if value in ('ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'joker') else 'undefined'
        self.__fpng = fpng
        self.__bpng = bpng

    def getSuit(self):
        return self.__suit
    def getValue(self):
        return  self.__value
    def getFrontPng(self):
        return self.__fpng
    def getBackPng(self):
        return self.__bpng