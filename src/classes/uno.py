from .deck import Deck, Card, Hand, Player

class UnoCard(Card):
    """
    Classe UnoCard feita para ser implementação da classe abstrata Card no formato de uma carta 
    de baralho de Uno convencional

    Atributos
    ---------
    Privados:
        value : str
        color : str

    Métodos
    -------
    color():
        Getter de color
    value():
        Getter de value
    value():
        Setter de value
    color():
        Setter de color
    match():
        Método para verificar se dois objetos UnoCard são "compatíveis" conforme as regras do Uno tradicional
    __str__:
        Sobrecarga do operador __str__ com o fim de realizar print modificado da classe
    """
    def __init__(self, value:str, color:str = '', frontSprite:str = '', backSprite:str = ''):
        """
        Construtor de um objeto UnoCard responsável por inicializar os atributos de um objeto UnoCard

        Args:
            value (str): string a ser utilizada como valor da carta tal qual um baralho de UNO convencional. Default como ''.
            color (str): string a ser utilizada como cor da carta tal qual um baralho de UNO convencional. Default como ''.
            frontSprite (str, optional): path a ser utilizado como frontSprite da carta. Default como ''.
            backSprite (str, optional): path a ser utilizado como backSprite da carta. Default como ''.
        """
        super().__init__(frontSprite, backSprite)
        self.__value = value
        self.__color = color

    @property
    def color(self):
        """
        Getter de color

        Returns:
            str: string atual sendo utilizada como cor em objeto UnoCard
        """
        return self.__color
    
    @property
    def value(self):
        """
        Getter de value

        Returns:
            str: string atual sendo utilizada como valor em objeto UnoCard
        """
        return self.__value
    
    @value.setter
    def value(self, value):
        """
        Setter de value

        Argumentos:
            value (str): string a ser utilizada como atributo de valor em UnoCard
        """
        self.__value = value

    @color.setter
    def color(self, color:str):
        """
        Setter de color

        Argumentos:
            color (str): string a ser utilizada como atributo de cor em StandardCard
        """
        if color in ('red', 'yellow', 'green', 'blue', '') and self.__value in ('wild', '+4'):
            self.__color = color
            if color == '':
                self._Card__sprite = f'{self.__value}'
            else:
                self._Card__sprite = f'{color}_{self.__value}'
    
    def match(self, card):
        """
        Método que irá realizar a operação de compatibilidade entre dois objetos UnoCard
        conforme as regras do UNO convencional

        Argumentos:
            card (UnoCard): objeto UnoCard a ser utilizado na operação de compatibilidade

        Returns:
            bool: valor booleano True para caso haja compatibilidade entre os objetos UnoCard,
                  False caso o contrário
        """
        if self.__color == '' or card.color == '':
            return True
        return self.__color == card.color or self.__value == card.value

    #SOBRECARGA DE OPERADOR
    def __str__(self):
        """
        Sobrecarga do operador __str__ com o intuito de modificar o resultado de um print()
        de um objeto UnoCard
        """
        if self._Card__faceUp:
            return f'{self.__color} {self.__value}' if self.__color else f'{self.__value}'
        else:
            return 'Face Down'

class UnoDeck(Deck):
    """
    Classe UnoDeck feita para ser implementação da classe abstrata Deck no formato de um 
    conjunto de cartas a serem utilizadas na mesa de um jogo utilizando baralho  de UNO convencional
    """
    def __init__(self):
        """
        Construtor de um objeto UnoDeck responsável por inicializar os atributos de um objeto UnoDeck
        """
        super().__init__()

    def createDeck(self):
        """
        Implementação do método abstrato createDeck para o formato da criação de um conjunto de cartas
        a serem utilizadas na mesa de um jogo de UNO utilizando baralho de UNO convencional
        """
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
    """
    Classe UnoHand feita para ser implementação da classe abstrata Hand no formato de um
    conjunto de cartas a serem utilizados por um jogador utilizando baralho de UNO convencional

    Métodos
    -------
    sumValues():
        Realiza a soma dos valores de um objeto UnoHand conforme as regras do Uno tradicional
    sort():
        Realiza a ordenação dos objetos UnoCard presentes em um objeto UnoHand conforme cor e valor
    """
    def __init__(self):
        """
        Construtor de um objeto UnoHand responsável por inicializar os atributos de um objeto UnoHand
        """
        super().__init__()

    def sumValues(self):
        """
        Método que irá realizar a soma dos valores de um objeto UnoHand conforme as regras do
        Uno tradicional, ou seja, irá somar as cartas da mão de um jogador

        Returns:
            int: Soma dos valores de um objeto UnoHand conforme as regras do Uno tradicional
        """
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
        """
        Método que irá realizar a ordenação dos objetos UnoCard de um objeto UnoHand conforme cor e valor
        """
        self.cards.sort(key=lambda card: (card.color, card.value))

class UnoPlayer(Player, UnoHand):
    """
    Classe UnoPlayer feita para ser implementação da classe abstrata Player e também
    herdando a classe UnoHand, ou seja, a classe UnoPlayer é um jogador de UNO
    utilizando um baralho de UNO convencional e as regras do UNO, além das informações do Player    
    """
    def __init__(self, name, points = 0):
        Player.__init__(self, name, points)
        UnoHand.__init__(self)

class UnoPlayers:
    """
    Classe UnoPlayers feita para ser o conjunto dos jogadores em uma mesa de UNO, conforme as regras
    do UNO e suas necessidades, OBS: é um conjunto fixo por utilizar apenas um jogador real e 3 bots

    Atributos
    ---------
    Privados:
        players : list[UnoPlayer]
        turn : int
        rotation : int
        already_buy : bool

    Métodos
    -------
    turn():
        Getter de turn
    rotation():
        Getter de rotation
    players():
        Getter de players
    already_buy()
        Getter de already_buy
    turn():
        Setter de turn
    rotation():
        Setter de rotation
    players():
        Setter de players
    already_buy():
        Setter de already_buy
    flipRotation():
        Realiza mudança no atributo rotation quando necessário
    setNextTurn():
        Realiza decisão para qual jogador será o próximo turno quando necessário
    clear():
        Realiza um reset nos atributos e jogadores utilizados
    getCurrentPlayer():
        Obtém qual o jogador no turno atual
    getNextPlayer():
        Obtém qual será o próximo jogador a jogar
    getNextTurn():
        Obtém qual será o próximo turno
    getHumanPlayer():
        Obtém o jogador que não é um bot dentre os demais
    __getitem__():
        sobrecarga do operador __getitem__ com o fim de modificar o acesso por índice da lista     
    """
    def __init__(self, playerName):
        """
        Construtor de um objeto UnoPlayers responsável por inicializar os atributos de um objeto UnoPlayers

        Argumentos:
            playerName (str): string a ser utilizada como nome do jogador
        """
        playersNames = [playerName, 'Bot1', 'Bot2', 'Bot3']

        self.__players = [UnoPlayer(name) for name in playersNames]
        self.__turn = 0
        self.__rotation = 1
        self.__already_buy = False

    @property
    def turn(self):
        """
        Getter de turn

        Returns:
            int: Valor int atual sendo utilizada para representar o turno em objeto UnoPlayers
        """
        return self.__turn
    
    @property
    def rotation(self):
        """
        Getter de rotation

        Returns:
            int: Valor int atual sendo utilizada para representar a rotação em objeto UnoPlayers
        """
        return self.__rotation

    @property
    def players(self):
        """
        Getter de players

        Returns:
            list[UnoPlayer]: lista de UnoPlayer atual sendo utilizada para representar a coleção 
                             de UnoPlayer em um objeto UnoPlayers
        """
        return self.__players
    
    @property
    def already_buy(self):
        """
        Getter de already_buy

        Returns:
            bool: valor booleano atual sendo utilizado para representar se já houve ou não a compra de 
                  cartas necessárias em um objeto UnoPlayers
        """
        return self.__already_buy

    @turn.setter
    def turn(self, turn):
        """
        Setter de turn

        Argumentos:
            turn (int): Valor int a ser utilizado como atributo de turn em UnoPlayers
        """
        self.__turn = turn
    
    @rotation.setter
    def rotation(self, rotation):
        """
        Setter de rotation

        Argumentos:
            rotation (int): Valor int a ser utilizado como atributo de rotation em UnoPlayers
        """
        self.__rotation = rotation

    @already_buy.setter
    def already_buy(self, already_buy):
        """
        Setter de already_buy

        Argumentos:
            already_buy (bool): Valor bool a ser utilizado como atributo de already_buy em UnoPlayers
        """
        self.__already_buy = already_buy
    
    @players.setter
    def players(self, players):
        """
        Setter de players

        Argumentos:
            players (list[UnoPlayer]): Valor bool a ser utilizado como atributo de already_buy em UnoPlayers
        """
        self.__players = players

    def flipRotation(self):
        """
        Método que irá realizar a mudança de rotação e do atributo rotation no jogo conforme as regras do UNO tradicional
        """
        self.__rotation *= -1    
    
    def setNextTurn(self):
        """
        Método que irá realizar a mudança de turno no jogo e do atributo turn conforme as regras do UNO tradicional
        """
        self.__turn = (self.__turn + self.__rotation) % len(self.__players)

    def clear(self):
        """
        Método que irá realizar o reset nos atributos e operação de clear() na lista 
        de jogadores em um objeto UnoPlayers 
        """
        self.__turn = 0
        self.__rotation = 1
        self.__already_buy = False
        for player in self.__players:
            player.clear()
    
    def getCurrentPlayer(self):
        """
        Método que irá obter qual o jogador atual na conforme os turnos do UNO

        Returns:
            UnoPlayer: Objeto UnoPlayer que representa o jogador atual do UNO
        """
        return self.__players[self.__turn]
    
    def getNextPlayer(self):
        """
        Método que irá obter qual o próximo jogador conforme os turnos e regras do UNO

        Returns:
            UnoPlayer: Objeto UnoPlayer que representa o próximo jogador do UNO
        """

        return self.__players[self.getNextTurn()]
    
    def getNextTurn(self):
        """
        Método que irá obter qual o próximo turno conforme os turnos e regras do UNO

        Returns:
            int: Valor int que representa o próximo turno do UNO
        """
        return (self.__turn + self.__rotation) % len(self.__players)
    
    def getHumanPlayer(self):
        """
        Método que irá obter o jogador "humano" do UNO

        Returns:
            UnoPlayer: Objeto UnoPlayer que representa o jogador humano do UNO
        """
        return self.__players[0]
    
    #SOBRECARGA DE OPERADOR
    def __getitem__(self, index):
        """
        Sobrecarga do operador __getitem__ com o intuito de modificar o resultado de um acesso
        por índice de um objeto UnoPlayers
        """
        return self.__players[index]

