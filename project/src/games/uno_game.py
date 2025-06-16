import random

from ..classes.uno import UnoDeck, UnoPlayer, UnoPlayers, UnoCard

SPECIAL_CARDS = ['+4', 'wild', '+2', 'reverse', 'block']
UNO_COLORS = ['red','yellow','green','blue']

class UnoGame:
    """
    Classe UnoGame feita para ser uma mesa de jogo conforme as regras de um
    jogo de Uno clássico, junto das ações e funções necessárias

    Atributos
    ---------
    Privados:
        players : UnoPlayers
        buy_deck : UnoDeck
        disc_deck : UnoDeck
        state : str

    Métodos
    -------
    players():
        Getter de players
    buy_deck():
        Getter de buy_deck
    disc_deck():
        Getter de disc_deck
    state():
        Getter de state
    players():
        Setter de players
    buy_deck():
        Setter de buy_deck
    disc_deck():
        Setter de disc_deck
    state():
        Setter de state
    start_round():
        Método responsável por começar um novo jogo de UNO
    next_turn():
        Método responsável por determinar de qual entidade será o próximo turno
    player_play_card():
        Método responsável por determinar a jogada a ser feita por um jogador ou bot
    human_select_color():
        Método responsável por determinar a cor a ser selecionada pelo jogador humano
    bot_select_color():
        Método responsável por determinar a cor a ser selecionada pelo jogador bot
    reshuffle_buy_deck():
        Método responsável por realizar um novo embaralhamento do baralho de compras de uma mesa de UNO
    draw_card():
        Método responsável por controlar a compra de uma carta advinda de um baralho de compras de uma mesa de UNO  
    player_draw_card():
        Método responsável por controlar a compra de uma carta feita pelo jogador advindo de um baralho de compras
        de uma mesa de UNO
    bot_play():
        Método responsável por determinar a jogada a ser feita de forma aleatória por um bot dentro da mesa de UNO
    sumPoints():
        Método responsável por obter a soma de pontuação das cartas conforme as regras do UNO clássico
    """
    #Private methods
    def __init__(self, player_name:str):
        """
        Construtor da classe UnoGame responsável por inicializar os atributos de um objeto UnoGame     
        """
        #Private atributes
        self.__players = UnoPlayers(player_name)
        self.__buy_deck = UnoDeck()
        self.__disc_deck = UnoDeck()
        self.__state = 'START' # Possible states: START, PLAYER_TURN, PLAYER_SELEC_COLOR, BOT_TURN, ,ROUND_OVER


    #Public methods
    @property
    def players(self):
        """
        Getter de players

        Returns:
            UnoPlayers: objeto UnoPLayers atual sendo utilizado para representar os jogadores em uma mesa de UNO
        """
        return self.__players
    
    @property
    def buy_deck(self):
        """
        Getter de buy_deck

        Returns:
            UnoDeck: objeto UnoDeck atual sendo utilizado para representar um baralho de UNO convencional sendo utilizado
                     como baralho de compra em um jogo de UNO
        """
        return self.__buy_deck
    
    @property
    def disc_deck(self):
        """
        Getter de disc_deck

        Returns:
            UnoDeck: objeto UnoDeck atual sendo utilizado para representar um baralho de UNO convencional sendo utilizado
                     como o baralho de descarte na mesa de UNO
        """
        return self.__disc_deck
    
    @property
    def state(self):
        """
        Setter de state

        Returns:
            str: str atual sendo utilizada para representar o estado atual do jogo, sendo os estados possíveis,
                 'START', 'PLAYER_TURN', 'PLAYER_SELEC_COLOR', 'BOT_TURN','' ,'ROUND_OVER'
        """
        return self.__state
    
    @players.setter
    def players(self, players):
        """
        Setter de players

        Argumentos:
            players (UnoPlayers): objeto UnoPLayers a ser utilizado para representar os jogadores em uma mesa de UNO
        """
        self.__players = players
    
    @buy_deck.setter
    def buy_deck(self, buy_deck):
        """
        Setter de buy_deck

        Returns:
            buy_deck (UnoDeck): objeto UnoDeck atual sendo utilizado para representar um baralho de UNO convencional 
                                a ser utilizada como baralho de compra em um jogo de UNO
        """
        self.__buy_deck = buy_deck
    
    @disc_deck.setter
    def disc_deck(self, disc_deck):
        """
        Getter de disc_deck

        Returns:
            disc_deck (UnoDeck): objeto UnoDeck atual sendo utilizado para representar um baralho de UNO convencional 
                                 a ser utilizado como o baralho de descarte na mesa de UNO
        """
        self.__disc_deck = disc_deck

    @state.setter
    def state(self, state:str):
        """
        Setter de state

        Returns:
            state str: str a ser utilizada para representar o estado atual do jogo, sendo os estados possíveis,
                 'START', 'PLAYER_TURN', 'PLAYER_SELEC_COLOR', 'BOT_TURN','' ,'ROUND_OVER'
        """
        self.__state = state

    def start_round(self):
        """
        Método que irá começar um novo jogo de UNO, inicializando os parâmetros necessários do jogo
        """
        for player in self.__players:
            player.points = 0
        self.__buy_deck.clear()
        self.__disc_deck.clear()
        self.__players.clear()
        self.__buy_deck.createDeck()
        self.__buy_deck.shuffle()

        for i in range(7):
            for player in self.__players:
                player.add(self.__buy_deck.give(player == self.__players.getHumanPlayer()))
                if player == self.__players.getHumanPlayer():
                    player.sort()

        self.__disc_deck.add(self.__buy_deck.give())

        while self.__disc_deck.topCard().value in SPECIAL_CARDS:
            self.__disc_deck.add(self.__buy_deck.give())

        self.__state = 'PLAYER_TURN'


    def next_turn(self):
        """
        Método que irá determinar de qual entidade será o próximo turno, ou seja, se o próximo
        turno será de um player ou bot
        """
        self.__players.setNextTurn()
        self.players.already_buy = False
        if self.__players.turn == self.players.getHumanTurn():
            self.__players.getCurrentPlayer().sort()
            self.__state = 'PLAYER_TURN'
        else:
            self.__state = 'BOT_TURN'

    def player_play_card(self, card_index):
        """
        Método que irá determinar a carta a ser jogada por um jogador ou bot

        Args:
            card_index (int): Valor int a ser utilizado como índice da carta a ser buscada
        """
        card:UnoCard = self.__players.getCurrentPlayer()[card_index]
        card.faceUp = True
        if self.__disc_deck.topCard().match(card):
            self.__disc_deck.add(self.__players.getCurrentPlayer().give(card))
            print(f'{self.__players.getCurrentPlayer().name}: played [{self.__disc_deck.topCard()}]')
            if self.__players.getCurrentPlayer().isEmpty():
                self.sumPoints()
                self.state = 'ROUND_OVER'
            else:
                if self.__disc_deck.topCard().value in SPECIAL_CARDS:
                    if self.__disc_deck.topCard().value in ['+4', 'wild']:
                        if self.__players.getCurrentPlayer() == self.__players.getHumanPlayer():
                            self.state = 'PLAYER_SELEC_COLOR'
                        else:
                            self.bot_select_color()
                    if self.__disc_deck.topCard().value == '+2':
                        for i in range(2):
                            self.draw_card(self.__players.getNextPlayer())
                    if self.__disc_deck.topCard().value in ['+2', 'block']:
                        self.__players.setNextTurn()
                    if self.__disc_deck.topCard().value == 'reverse':
                        self.__players.flipRotation()
                if not self.__disc_deck.topCard().value in ['+4', 'wild']:
                    self.next_turn()

    def human_select_color(self, color):
        """
        Método que irá determinar a cor a ser selecionada pelo jogador para a próxima jogada, fator 
        importante em um jogo de UNO, pois as regras são baseadas em cores e em números

        Args:
            color (str): string que representa a cor ou tipo da carta de UNO
        """
        if self.__disc_deck.topCard().color == '':
            self.__disc_deck.topCard().color = color
        if self.__disc_deck.topCard().value == '+4':
            for i in range(4):
                self.draw_card(self.__players.getNextPlayer())
            self.__players.setNextTurn()
        self.next_turn()
    
    def bot_select_color(self):
        """
        Método que irá determinar a cor a ser selecionada pelo bot para a próxima jogada, 
        de forma aleatória, fator importante em um jogo de UNO, pois as regras são 
        baseadas em cores e em números
        """
        if self.__disc_deck.topCard().color == '':
            for card in self.__players.getCurrentPlayer():
                if card.color != '':
                    self.__disc_deck.topCard().color = card.color
                    break
            else:
                self.__disc_deck.topCard().color = random.choice(UNO_COLORS)
        if self.__disc_deck.topCard().value == '+4':
            for i in range(4):
                self.draw_card(self.__players.getNextPlayer())
            self.__players.setNextTurn()
        self.next_turn()
                    
    def reshuffle_buy_deck(self):
        """
        Método que irá realizar um novo embaralhamento do baralho de compras de uma mesa de UNO a partir
        do baralho de descarte, ou seja, o baralho de descarte será embaralhado e após isso, utilizado como
        baralho de compras, no formato de regras do UNO
        """
        topCard = self.__disc_deck.give()
        topCard.flip()
        while not self.__disc_deck.isEmpty():
            if self.__disc_deck.topCard().value in ['+4', 'wild']:
                self.__disc_deck.topCard().color = ''
            self.__buy_deck.add(self.__disc_deck.give())
        self.__disc_deck.add(topCard)
        self.__buy_deck.shuffle()

    def draw_card(self, player):
        """
        Método que irá realizar a compra de uma carta no baralho de compras e caso não haja cartas no baralho
        de compras, haverá um embaralhamento do baralho de descarte

        Argumentos:
            player (UnoPlayer): objeto UnoPlayer o qual representa o jogador que irá receber a carta comprada
        """
        if self.__buy_deck.isEmpty():
            self.reshuffle_buy_deck()
        player.add(self.__buy_deck.give(player == self.__players.getHumanPlayer()))

    def player_draw_card(self, player):
        """
        Método que irá controlar a compra de uma carta feita pelo jogador advindo de um baralho de compras
        de uma mesa de UNO e irá retornar o indíce da carta obtida para reorganização

        Argumentos:
            player (UnoPlayer): jogador que irá realizar a compra da carta

        Returns:
            int: posição da carta obtida na compra, caso não seja obtida, retornará -1
        """
        self.players.already_buy = True
        self.draw_card(player)
        for card in player:
            if card.match(self.__disc_deck.topCard()):
                return player.cards.index(card)
        else:
            self.next_turn()
        print(f'{player.name}: drew a card, ({self.__buy_deck.size()} cards left in the buy deck)')
        return -1

    def bot_play(self):
        """
        Método responsável por determinar a jogada a ser feita de forma aleatória por um bot dentro da mesa de UNO
        """
        for i, card in enumerate(self.__players.getCurrentPlayer().cards):
            if card.match(self.__disc_deck.topCard()):
                self.player_play_card(i)
                break
        else:
            buy_card_index = self.player_draw_card(self.__players.getCurrentPlayer())
            if buy_card_index != -1:
                self.player_play_card(buy_card_index)

    def sumPoints(self):
        """
        Método responsável por somar os pontos obtidos ao player humano da mesa conforme as regras 
        do UNO clássico 
        """
        for player in self.__players:
            self.players.getCurrentPlayer().points += player.sumValues() 
        
