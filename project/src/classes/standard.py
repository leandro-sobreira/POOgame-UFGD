from .deck import Deck, Card, Hand, Player 

class StandardCard(Card):
    """
    Classe StandardCard feita para ser implementação da classe abstrata Card no formato de uma carta 
    de baralho convencional

    Atributos
    ---------
    Privados:
        suit : str
        value : str

    Métodos
    -------
    suit():
        Getter de suit
    value():
        Getter de value
    suit():
        Setter de suit
    value():
        Setter de value
    __str__:
        Sobrecarga do operador __str__ com o fim de realizar print modificado da classe
    """
    def __init__(self, suit:str, value:str, frontSprite:str = 'joker', backSprite:str = 'joker'): #
        """
        Construtor de um objeto StandardCard responsável por inicializar os atributos de um objeto StandardCard

        Args:
            suit (str): string a ser utilizada como naipe da carta tal qual um baralho convencional
            value (str): string a ser utilizada como valor da carta tal qual um baralho convencional
            frontSprite (str, optional): path a ser utilizado como frontSprite da carta. Default como 'joker'.
            backSprite (str, optional): path a ser utilizado como backSprite da carta. Default como 'joker'.
        """
        super().__init__(frontSprite, backSprite) #
        self.__suit = suit #
        self.__value = value #

    @property
    def suit(self): #
        """
        Getter de suit

        Returns:
            str: string atual sendo utilizada como naipe em objeto StandardCard
        """
        return self.__suit
    
    @property
    def value(self): #
        """
        Getter de value

        Returns:
            str: string atual sendo utilizada como valor em objeto StandardCard
        """
        return self.__value
    
    @suit.setter
    def suit(self, suit):
        """
        Setter de suit

        Argumentos:
            suit (str): string a ser utilizada como atributo de naipe em StandardCard
        """
        self.__suit = suit
    
    @value.setter
    def value(self, value):
        """
        Setter de value

        Argumentos:
            value (str): string a ser utilizada como atributo de valor em StandardCard
        """
        self.__value = value    

    #SOBRECARGA DE OPERADOR
    def __str__(self): #
        """
        Sobrecarga do operador __str__ com o intuito de modificar o resultado de um print()
        de um objeto StandardCard
        """
        if self.getFace(): #
            return f'{self.__value} of {self.__suit}' #
        else:
            return 'Face Down' #

class StandardDeck(Deck): #
    """
    Classe StandardDeck feita para ser implementação da classe abstrata Deck no formato de um 
    conjunto de cartas a serem utilizadas na mesa de um jogo utilizando baralho convencional
    """
    def __init__(self): #
        """
        Construtor de um objeto StandardDeck responsável por inicializar os atributos de um objeto StandardDeck
        """
        super().__init__() #

    def createDeck(self): #
        """
        Implementação do método abstrato createDeck para o formato da criação de um conjunto de cartas
        a serem utilizadas na mesa de um jogo utilizando baralho convencional
        """
        suits = ['heart', 'diamond', 'club', 'spade'] #
        values = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king'] #
        
        for suit in suits: #
            for value in values: #
                self.add(StandardCard(suit=suit, value=value, frontSprite=f'{value}_of_{suit}', backSprite='cardBack_red5')) #

class StandardHand(Hand): #
    """
    Classe StandardHand feita para ser implementação da classe abstrata Hand no formato de um
    conjunto de cartas a serem utilizados por um jogador utilizando baralho convencional

    Métodos
    -------
    sumValues():
        Realiza a soma dos valores de um objeto StandardHand conforme as regras do BlackJack tradicional (21)
    """
    def __init__(self): #
        """
        Construtor de um objeto StandardHand responsável por inicializar os atributos de um objeto StandardHand
        """
        super().__init__() #

    def sumValues(self): #
        """
        Método que irá realizar a soma dos valores de um objeto StandardHand conforme as regras do
        BlackJack tradicional (ou 21), ou seja, irá somar as cartas da mão de um jogador

        Returns:
            int: Soma dos valores de um objeto StandardHand conforme as regras do BlackJack tradicional
                (ou 21)
        """
        total = 0 #
        aces_appears = False 
        for card in self.cards: #
            if card.faceUp: #
                value = card.value #
                if value in ('jack', 'queen', 'king'): #
                    total += 10 #
                elif value == 'ace': #
                    aces_appears = True #
                    total += 1
                else:
                    total += int(value) #
        
        # Adjust for aces if total is under 12 #
        if total < 12 and aces_appears:
            total += 10 #
        return total #

class StandardPlayer(Player, StandardHand):
    """
    Classe StandardPlayer feita para ser implementação da classe abstrata Player e também
    herdando a classe StandardHand, ou seja, a classe StandardPlayer é um jogador de baralho
    utilizando um baralho convencional e as regras do 21, além das informações do Player    
    """
    def __init__(self, name, points=1000):
        """
        Construtor de um objeto StandardPlayer responsável por inicializar os atributos de um objeto StandardPlayer

        Argumentos:
            name (str): string sendo utilizada como nome do jogador
            points (int, optional): Valor int sendo utilizado como a quantidade de pontos de um jogador. 
                                    Default como 1000.
        """
        Player.__init__(self, name, points) 
        StandardHand.__init__(self) 
