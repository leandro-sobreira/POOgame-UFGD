import random
from abc import ABC, abstractmethod

class Card(ABC):
    """
    Classe abstrata Card feita para ser uma abstração de uma carta genérica qualquer

    Atributos
    ---------
    Privados:
        frontSprite : str
        backSprite : str
        sprite : str
        faceUp : bool

    Métodos
    -------
    frontSprite():
        Getter de frontSprite
    backSprite():
        Getter de backSprite
    sprite():
        Getter de sprite
    faceUp():
        Getter de faceUp
    frontSprite():
        Setter de frontSprite
    backSprite():
        Setter de backSprite
    sprite():
        Setter de sprite
    faceUp():
        Setter de faceUp
    flip():
        Realiza o flip de uma carta, ou seja, realiza a mudança de sprite e do atributo faceUp
    """
    def __init__(self, frontSprite:str= '', backSprite:str= ''):
        """
        Construtor da classe abstrata Card responsável por inicializar os atributos de um objeto Card        

        Argumentos:
            frontSprite (str, optional): path do sprite a ser utilizado como frontSprite. Default como ''.
            backSprite (str, optional): path do sprite a ser utilizado como backSprite. Default como ''.
        """
        self.__frontSprite = frontSprite
        self.__backSprite = backSprite
        self.__sprite = backSprite
        self.__faceUp:bool = False

    @property
    def frontSprite(self):
        """
        Getter de frontSprite

        Returns:
            str: path do sprite sendo utilizado como frontSprite
        """
        return self.__frontSprite
    
    @property
    def backSprite(self):
        """
        Getter de backSprite

        Returns:
            str: path do sprite sendo utilizado como backSprite
        """
        return self.__backSprite
    
    @property
    def sprite(self):
        """
        Getter de sprite

        Returns:
            str: path do sprite sendo utilizado como sprite
        """
        return self.__sprite
    
    @property
    def faceUp(self):
        """
        Getter de faceUp

        Returns:
            bool: valor booleano atual sendo utilizado como faceUp
        """
        return self.__faceUp
    
    @frontSprite.setter
    def frontSprite(self, frontSprite):
        """
        Setter de frontSprite

        Args:
            frontSprite (str): path do frontSprite a ser utilizado 
        """
        self.__frontSprite = frontSprite

    @backSprite.setter
    def backSprite(self, backSprite):
        """
        Setter de backSprite

        Args:
            backSprite (str): path do backSprite a ser utilizado 
        """
        self.__backSprite = backSprite
    
    @sprite.setter
    def sprite(self, sprite):
        """
        Setter de sprite

        Args:
            sprite (str): path do sprite a ser utilizado 
        """
        self.__sprite = sprite
    
    @faceUp.setter    
    def faceUp(self, faceUp:bool):
        """
        Setter de faceUp, também irá atualizar o atributo sprite baseado 
        nos atributos fronSprite ou backSprite

        Args:
            faceUp (bool): valor booleano a ser utilizado em faceUp
        """
        self.__faceUp = faceUp

        if faceUp:
            self.__sprite = self.__frontSprite
        else:
            self.__sprite = self.__backSprite

    def flip(self):
        """
        Método que irá realizar a operação de flip em uma carta, ou seja,
        irá inverter o valor de faceUp e realizar a mudança de sprite
        """
        self.__faceUp = self.__faceUp == False
        if self.__faceUp:
            self.__sprite = self.__frontSprite
        else:
            self.__sprite = self.__backSprite


class Deck(ABC):
    """
    Classe abstrata Deck feita para ser uma abstração de um conjunto de cartas (baralho)
    e um container de classes Card ou herdadas de Card a ser utilizado na mesa de um jogo

    Há polimorfismo paramétrico e sobrecarga de operador nesta classe

    Atributos
    ---------
    Privados:
        cards : list[Card]

    Métodos
    -------
    cards():
        Getter de frontSprite
    cards():
        Setter de backSprite
    topCard():
        Método para obter objeto Card na última posição de um Deck
    isEmpty():
        Método para obter informação se um objeto Deck está ou não vazio
    add():
        Método para adicionar um objeto Card a um objeto Deck
    __iadd()__:
        Sobrecarga de método com o fim de adicionar um objeto Card a um objeto Deck
    discard():
        Método para realizar pop() em um objeto Deck
    clear():
        Método para realizar clear() em um objeto Deck
    size():
        Método para realizar len() em um objeto Deck
    give():
        Método para obter qual objeto Card será entregue a outra entidade do sistema
        e realizar discard() da mesma
    shuffle():
        Método para realizar random.shuffle() de um objeto Deck
    createDeck():
        Método ABSTRATO para criação de um objeto Deck
    """
    def __init__(self):
        """
        Construtor de um objeto Deck responsável por inicializar os atributos de um objeto Deck
        """ 
        self.__cards = []

    @property
    def cards(self):
        """
        Getter de cards

        Returns:
            list[Card]: list atual contendo objetos Card sendo utilizados como atributo de Deck
        """
        return self.__cards
    
    @cards.setter
    def cards(self, cards):
        """
        Setter de cards

        Argumentos:
            cards (list[Card]): list contendo objetos Card a serem utilizados como atributo de Deck
        """
        self.__cards = cards

    def topCard(self):
        """
        Método que irá retornar a carta no topo de um baralho, ou seja, o objeto Card
        que está na última posição de um objeto Deck, respeitando a ordem LIFO de uma pilha

        Returns:
            Card: objeto Card na última posição de um objeto Deck
        """
        return self.__cards[-1]

    def isEmpty(self):
        """
        Método que irá retornar um valor booleano para os casos de um objeto Deck
        estar ou não vazio

        Returns:
            bool: valor booleano True para caso o objeto Deck esteja vazio e False caso contrário
        """
        return not self.__cards

    #POLIMORFISMO PARAMÉTRICO
    def add(self, card):
        """
        Método que irá realizar operação de append em um objeto Deck, ou seja, irá
        acrescentar a carta desejada a um baralho

        Argumentos:
            card (Card): objeto Card a ser adicionado em um objeto Deck

        Raises:
            TypeError: será interrompida a execução caso um objeto que não seja do tipo
                       Card ou herdado de Card seja utilizado neste método
        """
        if(isinstance(card, Card)):
            self.__cards.append(card)
        else:
            raise TypeError("Append de classe errada para o conteiner Hand!")

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

    #POLIMORFISMO PARAMÉTRICO
    def add(self, card):

        if(isinstance(card, Card)):
            self.__cards.append(card)
        else:
            #raise TypeError("Append de classe errada para o conteiner Hand!")
            pass
    
    #SOBRECARGA DE OPERADOR
    def __iadd__(self, card):
        self.add(card)

    #SOBRECARGA DE OPERADOR
    def __getitem__(self, item):
        return self.__cards[item]

    @property
    def cards(self):
        return self.__cards
    
    @cards.setter
    def cards(self, cards):
        self.__cards = cards

    def size(self):
        return len(self.__cards)

    def give(self, card):
        self.__cards.remove(card)

        return card
    
    def clear(self):
        self.__cards.clear()

    def flipAll(self, stat): #True to front up
        for card in self.__cards:
            if card.faceUp != stat:
                card.flip()


class Player(ABC):
    def __init__(self, name: str, points: int = 0):
        #super().__init__()
        self.__name = name
        self.__points = points

    @property
    def name(self):
        return self.__name

    @property
    def points(self):
        return self.__points
    
    @name.setter
    def name(self, name):
        self.__name = name
    
    @points.setter
    def points(self, points):
        self.__points = points

    def addPoints(self, amount: int):
        self.__points += amount

    #SOBRECARGA DE OPERADOR
    def __iadd__(self, amount: int):
        self.addPoints(amount)

    def remPoints(self, amount: int):
        #Adicionar tratamento de erro
        self.__points -= amount

    #SOBRECARGA DE OPERADOR
    def __isub__(self, amount: int):
        self.remPoints(amount)

    def givePoints(self, amount:int):
        self.remPoints(amount)
        
        return amount