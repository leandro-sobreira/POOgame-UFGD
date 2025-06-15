from ..classes.standard import StandardDeck, StandardPlayer

class BlackjackGame:
    """
    Classe BlackjackGame feita para ser uma mesa de jogo conforme as regras de um
    jogo de BlackJack clássico (ou 21), junto das ações e funções necessárias

    Atributos
    ---------
    Privados:
        player : StandardPlayer
        table : StandardPlayer
        gameDeck : StandardDeck
        betAmount : int
        state : str
        result : str

    Métodos
    -------
    player():
        Getter de player
    table():
        Getter de table
    gameDeck():
        Getter de gameDeck
    betAmount():
        Getter de betAmount
    state():
        Setter de state
    state():
        Setter de state
    result():
        Setter de result
    player():
        Setter de player
    table():
        Setter de table
    gameDeck():
        Setter de gameDeck
    betAmount():
        Setter de betAmount
    state():
        Setter de state
    state():
        Setter de state
    result():
        Setter de result
    setBetAmount():
        Método responsável por inicializar o jogo a partir de uma aposta 
    give_start_cards():
        Método responsável por distribuir as cartas iniciais do jogo
    start_round():
        Método responsável por iniciar um novo round do jogo
    player_hit():
        Método responsável para a solicitação de uma nova carta
    player_stand():
        Método responsável pela mudança de turno no qual o jogador permanece e o bot joga
    _dealer_play():
        Método responsável por determinar as jogadas do bot
    _determine_winner():
        Método responsável por determinar o vencedor do jogo
    get_player_data():
        Método responsável por obter os dados do jogador
    """
    def __init__(self, player_name:str):
        """
        Construtor de um objeto BlackjackGame e responsável por inicializar os atributos de um objeto BlackjackGame
        """
        self.__player = StandardPlayer(player_name, 1000) 
        self.__table = StandardPlayer("Dealer")
        self.__gameDeck = StandardDeck() 
        self.__betAmount = 0

        
        self.__state = "BET" # Possible states: PLAYER_TURN, DEALER_TURN, ROUND_OVER 
        self.__result = "" # e.g., "Player Wins!", "Bust!", "Push!" 

        self.setBetAmount()

    @property
    def player(self):
        """
        Getter de player

        Returns:
            StandardPlayer: objeto StandardPlayer atual sendo utilizado para representar o jogador em BlackjackGame
        """
        return self.__player
    
    @property
    def table(self):
        """
        Getter de table

        Returns:
            StandardPlayer: objeto StandardPlayer atual sendo utilizado para representar a table, ou seja, 
                            o outro jogador em BlackjackGame
        """
        return self.__table
    
    @property
    def gameDeck(self):
        """
        Getter de gameDeck

        Returns:
            StandardDeck: objeto StandardDeck atual sendo utilizado para representar um baralho convencional em mesa
        """
        return self.__gameDeck
    
    @property
    def win_value(self):
        return self.__win_value
    
    @property
    def betAmount(self):
        """
        Getter de betAmount

        Returns:
            int: Valor int atual sendo utilizado para representar a quantidade em aposta na mesa
        """
        return self.__betAmount
    
    @property
    def state(self):
        """
        Getter de state

        Returns:
            str: string atual sendo utilizada para representar o estado no qual o jogo se encontra, sendo
                 estes os possíveis estados:  "BET", "PLAYER_TURN", "DEALER_TURN", "ROUND_OVER" 
        """
        return self.__state
    
    @property
    def result(self):
        """
        Getter de result

        Returns:
            str: string atual sendo utilizada para representar o resultado final do jogo, sendo
                 estes os possíveis estados:  "Player Wins!", "Bust!", "Push! 
        """
        return self.__result
    
    @player.setter
    def player(self, player):
        """
        Setter de player

        Argumentos:
            player (StandardPlayer): objeto StandardPlayer a ser utilizado para representar a table, ou seja, 
                                     o outro jogador em BlackjackGame
        """
        self.__player = player
    
    @table.setter
    def table(self, table):
        """
        Setter de table

        Argumentos:
            table (StandardPlayer): objeto StandardPlayer a ser utilizado para representar a table, ou seja, 
                                    o outro jogador em BlackjackGame
        """
        self.__table = table
    
    @gameDeck.setter
    def gameDeck(self, gameDeck):
        """
        Setter de gameDeck

        Argumentos:
            gameDeck (StandardDeck): objeto StandardDeck a ser utilizado para representar um baralho convencional em mesa
        """
        self.__gameDeck = gameDeck
    
    @betAmount.setter
    def betAmount(self, betAmount):
        """
        Setter de betAmount

        Argumentos:
            betAmount (int): Valor int atual a ser utilizado para representar a quantidade em aposta na mesa
        """
        self.__betAmount = betAmount
    
    @state.setter
    def state(self, state):
        """
        Setter de state

        Argumentos:
            state (str): string a ser utilizada para representar o resultado final do jogo, sendo
                         estes os possíveis estados:  "Player Wins!", "Bust!", "Push! 
        """
        self.__state = state
    
    @result.setter
    def result(self, result):
        """
        Setter de result

        Argumentos:
            result (str): string atual a ser utilizada para representar o resultado final do jogo, sendo
                          estes os possíveis estados:  "Player Wins!", "Bust!", "Push!  
        """
        self.__result = result

    def setBetAmount(self):
        """
        Método que irá inicializar o jogo e irá começar o jogo em estado inicial a partir de uma determinada aposta 
        """
                
        if self.__betAmount < 10 or self.__betAmount > self.__player.points:
            self.__state = "BET"
        else:
            self.start_round()

    # Deal initial cards  animation#
    def give_start_cards(self):
        """
        Método que irá distribuir as cartas iniciais do jogo conforme as regras tradicionais do BlackJack (ou 21)
        para o jogador e o bot (dealer)
        """
        if self.__table.size() == 0:
            self.__table.add(self.__gameDeck.give())
        elif self.__table.size() == 1:
            if self.__player.size() == 0:
                self.__player.add(self.__gameDeck.give())
            elif self.__player.size() == 1:
                self.__table.add(self.__gameDeck.give(False))
        elif self.__table.size() == 2:
            if self.__player.size() == 1:
                self.__player.add(self.__gameDeck.give())
            if self.__player.size() == 2:
                self.__state = "PLAYER_TURN"


        # Check for immediate Blackjack 
        if self.__player.sumValues() == 21: 
            self.player_stand() 
    
    def start_round(self): 
        """
        Método responsável por iniciar um novo round do jogo, além de remover os pontos a partir da aposta realizada, resetar
        os atributos utilizados plea classe BlackjackGame e começar um novo jogo
        """
        self.__state = "START" 
        self.__result = "" 

        # Player pays the bet 
        self.__player.remPoints(self.__betAmount) 

        # Clear hands and deck 
        self.__win_value = 0
        self.__player.clear() 
        self.__table.clear() 
        self.__gameDeck.clear() 
        self.__gameDeck.createDeck() 
        self.__gameDeck.shuffle() 

        # Deal initial cards 
        

    def player_hit(self): 
        """
        Método que irá solicitar uma nova carta do baralho ao jogar e realizar as operações 
        necessárias conforme as regras do BlackJack (ou 21)
        """
        if self.__state == "PLAYER_TURN": 
            self.__player.add(self.__gameDeck.give()) 
            if self.__player.sumValues() > 21: 
                self.__result = "Player Busts! Dealer Wins." 
                self._determine_winner()
            elif self.__player.sumValues() == 21: 
                self.player_stand() 

    def player_stand(self): 
        """
        Método que irá realizar a mudança de turno no qual o jogador permanece e o bot (dealer) joga
        """
        if self.__state == "PLAYER_TURN": 
            self.__state = "DEALER_TURN" 

    def _dealer_play(self): 
        """
        Método que irá determinar as jogadas automáticas do bot (dealer) conforme as regras do BlackJack
        """
        if not self.__table[1].faceUp:
            self.__table.flipAll(True) # Reveal the dealer's hole card 
        else:
            if self.__table.sumValues() and self.__table.sumValues() < 17:
                self.__table.add(self.__gameDeck.give()) 
            else:
                self._determine_winner() #    

    def _determine_winner(self): 
        """
        Método que irá determinar o vencedor do jogo conforme os resultados finais gerados conforme
        as regras do BlackJack e realizar a mudança dos atributos necessários para confirmar a situação
        """
        player_score = self.__player.sumValues() 
        dealer_score = self.__table.sumValues() 

        if player_score > 21: # This case is already handled but good for clarity 
            self.__result = "Player Busts! Dealer Wins." 
        elif dealer_score > 21: 
            self.__result = "Dealer Busts! Player Wins." 
            self.__win_value = self.__betAmount * 2 # Return bet + winnings 
        elif player_score > dealer_score: 
            self.__result = "Player Wins!" 
            self.__win_value = self.__betAmount * 2
        elif dealer_score > player_score: 
            self.__result = "Dealer Wins." 
        else: # Push 
            self.__result = "Push (Draw)." 
            self.__win_value = self.__betAmount
        self.__player.addPoints(self.__win_value) # Return original bet 
        
        self.__betAmount = 0
        self.__state = "ROUND_OVER" 

    def get_player_data(self): 
        """
        Método que irá obter os dados do jogador para operações necessárias

        Returns:
            dict{key: str, key: str}: Dicionário python com as informações do jogador, sendo 
                                      estar o nome e a quantidade de pontos obtidos no blackjack
        """
        return { 
            "name": self.__player.name, 
            "blackjack_points": self.__player.points, 
            # Include other game scores here if they were part of the original data 
        }