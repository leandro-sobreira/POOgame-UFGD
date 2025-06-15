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
        Getter de cards
    cards():
        Setter de cards
    topCard():
        Método para obter objeto Card na última posição de um objeto Deck
    isEmpty():
        Método para obter informação se um objeto Deck está ou não vazio
    add():
        Método para adicionar um objeto Card a um objeto Deck
    __iadd()__:
        Sobrecarga de operador com o fim de adicionar um objeto Card a um objeto Deck
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
        """
        Sobrecarga do operador __iadd__ com o intuito de facilitar o uso do método add(),
        vide o método add() para a documentação completa

        Args:
            card (Card): objeto Card a ser adicionado em um objeto Deck
        """
        self.add(card)

    def discard(self):
        """
        Método que irá realizar a operação pop() do objeto Deck, ou seja, irá realizar
        o descarte de um elemento da lista conforme a ordem LIFO de uma pilha
        """
        self.__cards.pop()

    def clear(self):
        """
        Método que irá realizar a operação clear() do objeto Deck, ou seja, irá
        realizar o descarte total da lista
        """
        self.__cards.clear()

    def size(self):
        """
        Método que irá realizar a operação size() do objeto Deck, ou seja, irá
        retornar a quantidade de elementos presentes 

        Returns:
            int: quantidade de elementos em um objeto Deck
        """
        return len(self.__cards)

    def give(self, flip:bool = True):
        """
        Método que irá realizar o descarte da carta no topo de um baralho 
        e que será entregue como retorno da função para usos futuros

        Argumentos:
            flip (bool, optional): valor booleano representando se será realizado 
                                   a operação de flip no objeto Card a ser retornado. 
                                   Default como True.

        Returns:
            Card: objeto Card a ser entregue 
        """
        if not self.isEmpty() :
            card = self.__cards[-1]
            if flip:
                card.flip()
            self.discard()
            return card
        return None

    def shuffle(self):
        """
        Método que irá realizar a operação random.shuffle em um objeto Deck, ou seja,
        irá embaralhar o baralho utilizado
        """
        random.shuffle(self.__cards)

    @abstractmethod
    def createDeck(self):
        """
        Método ABSTRATO para a criação de um objeto Deck
        """
        pass

class Hand(ABC):
    """
    Classe abstrata Hand feita para ser uma abstração de um conjunto de cartas (baralho)
    e um container de classes Card ou herdadas de Card a ser utilizado por um jogador

    Há polimorfismo paramétrico e sobrecarga de operador nesta classe

    Atributos
    ---------
    Privados:
        cards : list[Card]

    Métodos
    -------
    cards():
        Getter de cards
    cards():
        Setter de cards
    topCard():
        Método para obter objeto Card na última posição de um objeto Hand
    isEmpty():
        Método para obter informação se um objeto Hand está ou não vazio
    add():
        Método para adicionar um objeto Card a um objeto Hand
    __iadd()__:
        Sobrecarga de operador com o fim de adicionar um objeto Card a um objeto Hand
    __getitem()__:
        Sobrecarga de operador com o fim de acessar determinado elemento de um objeto Hand
    size():
        Método para realizar len() em um objeto Hand
    give():
        Método para remover determinada Card de um objeto Deck e retorná-la como valor
        do método
    clear():
        Método para realizar clear() em um objeto Hand
    FlipAll():
        Método para realizar operação de flip() em todo os objetos Card de um objeto Hand

    """
    def __init__(self):
        """
        Construtor de um objeto Hand responsável por inicializar os atributos de um objeto Hand
        """ 
        self.__cards = []

    @property
    def cards(self):
        """
        Getter de cards

        Returns:
            list[Card]: list atual contendo objetos Card sendo utilizados como atributo de Hand
        """
        return self.__cards
    
    @cards.setter
    def cards(self, cards):
        """
        Setter de cards

        Argumentos:
            cards (list[Card]): list contendo objetos Card a serem utilizados como atributo de Hand
        """
        self.__cards = cards

    def isEmpty(self):
        """
        Método que irá retornar um valor booleano para os casos de um objeto Hand
        estar ou não vazio

        Returns:
            bool: valor booleano True para caso o objeto Hand esteja vazio e False caso contrário
        """
        return not self.__cards

    #POLIMORFISMO PARAMÉTRICO
    def add(self, card):
        """
        Método que irá realizar operação de append em um objeto Hand, ou seja, irá
        acrescentar a carta desejada a um baralho

        Argumentos:
            card (Card): objeto Card a ser adicionado em um objeto Hand

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
        """
        Sobrecarga do operador __iadd__ com o intuito de facilitar o uso do método add(),
        vide o método add() para a documentação completa

        Args:
            card (Card): objeto Card a ser adicionado em um objeto Hand
        """
        self.add(card)

    #SOBRECARGA DE OPERADOR
    def __getitem__(self, item):
        """
        Sobrecarga do operador __geitem__ com o intuito de facilitar o uso do acesso por posição

        Args:
            item (int): Posição desejada para acesso

        Returns:
            Card: objeto Card presente na posição item de um objeto Hand
        """
        return self.__cards[item]

    def size(self):
        """
        Método que irá realizar a operação size() do objeto Hand, ou seja, irá
        retornar a quantidade de elementos presentes 

        Returns:
            int: quantidade de elementos em um objeto Hand
        """
        return len(self.__cards)

    def give(self, card):
        """
        Método que irá realizar o descarte de uma carta específica de um objeto Hand 
        e que será entregue como retorno da função para usos futuros

        Argumentos:
            card (Card): objeto Card a ser removido do objeto Hand e entregue como retorno
                         da função

        Returns:
            Card: objeto Card a ser removido e entregue 
        """
        self.__cards.remove(card)

        return card
    
    def clear(self):
        """
        Método que irá realizar a operação clear() do objeto Hand, ou seja, irá
        realizar o descarte total da lista
        """
        self.__cards.clear()

    def flipAll(self, stat): #True to front up
        """
        Método que irá realizar a operação de flip() para todos os objetos Card presentes
        no objeto Hand

        Args:
            stat (bool): Será o valor booleano que irá ser usado na verificação do atributo card.FaceUp
                         para a operação de flip()
        """
        for card in self.__cards:
            if card.faceUp != stat:
                card.flip()


class Player(ABC):
    """
    Classe abstrata Player feita para ser uma abstração de um jogador genérico

    Há sobrecarga de operador nesta classe

    Atributos
    ---------
    Privados:
        name : str
        points : int

    Métodos
    -------
    name():
        Getter de name
    points():
        Getter de points
    name():
        Setter de name
    points():
        Setter de points
    addPoints():
        Método para adicionar pontos
    __iadd__():
        Sobrecarga de operador com o fim de adicionar pontos
    remPoints():
        Método para subtrair pontos
    __isub__():
        Sobrecarga de operador com o fim de subtrair pontos
    givePoints():
        Método para subtrair pontos de um objeto Player a partir de um montante
        e também retornar o montante

    """
    def __init__(self, name: str, points: int = 0):
        """
        Construtor de um objeto Player responsável por inicializar os atributos de um objeto Player

        Argumentos:
            name (str) : O nome a ser utilizado pelo player no formato string
            points (int) : A quantidade de pontos iniciais de um player, default como 0
        """ 
        self.__name = name
        self.__points = points

    @property
    def name(self):
        """
        Getter de name

        Returns:
            str: string atual sendo utilizada como atributo de name
        """
        return self.__name

    @property
    def points(self):
        """
        Getter de points

        Returns:
            int: Valor int atual sendo utilizado como atributo de points
        """
        return self.__points
    
    @name.setter
    def name(self, name):
        """
        Setter de cards

        Argumentos:
            name (str): str a ser utilizado como atributo name de Player
        """
        self.__name = name
    
    @points.setter
    def points(self, points):
        """
        Setter de points

        Argumentos:
            points (int): Valor int a ser utilizado como atributo points de Player
        """
        self.__points = points

    def addPoints(self, amount: int):
        """
        Método que irá adicionar um determinado montante ao atributo points de um Player

        Argumentos:
            amount (int): Valor int a ser adicionado ao atributo points de Player
        """
        self.__points += amount

    #SOBRECARGA DE OPERADOR
    def __iadd__(self, amount: int):
        """
        Sobrecarga do operador __iadd__ com o intuito de facilitar o uso do método addPoints(),
        vide o método addPoints() para a documentação completa

        Args:
            amount (int): Valor int a ser adicionado ao atributo points de Player
        """
        self.addPoints(amount)

    def remPoints(self, amount: int):
        """
        Método que irá subtrair um determinado montante ao atributo points de um Player

        Argumentos:
            amount (int): Valor int a ser subtraído ao atributo points de Player
        """
        self.__points -= amount

    #SOBRECARGA DE OPERADOR
    def __isub__(self, amount: int):
        """
        Sobrecarga do operador __isub__ com o intuito de facilitar o uso do método remPoints(),
        vide o método remPoints() para a documentação completa

        Args:
            amount (int): Valor int a ser subtraído ao atributo points de Player
        """
        self.remPoints(amount)

    def givePoints(self, amount:int):
        """
        Método que irá subtrair um determinado montante do atributo points de Player e irá 
        retornar o mesmo montante como valor da função

        Args:
            amount (int): Valor int a ser subtraído ao atributo points de Player e devolvido
                          como retorno da função

        Returns:
            int: Valor int do montante que foi utilizado
        """
        self.remPoints(amount)
        
        return amount