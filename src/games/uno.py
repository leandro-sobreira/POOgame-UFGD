import random

from ..classes.uno import UnoDeck, UnoPlayer, UnoPlayers, UnoCard

SPECIAL_CARDS = ['+4', 'wild', '+2', 'reverse', 'block']
UNO_COLORS = ['red','yellow','green','blue']

class UnoGame:
    
    #Private methods
    def __init__(self, player_data):

        #Private atributes
        self.__players = UnoPlayers(player_data['name'])
        self.__buy_deck = UnoDeck()
        self.__disc_deck = UnoDeck()
        self.__state = 'START' # Possible states: START, PLAYER_TURN, PLAYER_SELEC_COLOR, BOT_TURN, ,ROUND_OVER


    #Public methods
    @property
    def players(self):
        return self.__players
    
    @property
    def buy_deck(self):
        return self.__buy_deck
    
    @property
    def disc_deck(self):
        return self.__disc_deck
    
    @property
    def state(self):
        return self.__state
    
    @players.setter
    def players(self, players):
        self.__players = players
    
    @buy_deck.setter
    def buy_deck(self, buy_deck):
        self.__buy_deck = buy_deck
    
    @disc_deck.setter
    def disc_deck(self, disc_deck):
        self.__disc_deck = disc_deck

    @state.setter
    def state(self, state:str):
        self.__state = state

    def start_round(self):
        self.__buy_deck.clear()
        self.__disc_deck.clear()
        self.__players.clear()
        self.__buy_deck.createDeck()
        self.__buy_deck.shuffle()

        for i in range(7):
            for player in self.__players:
                #TODO: Saber qual é o problema 
                ##############################PROBLEMA
                #print(player, dir(player))

                player.add(self.__buy_deck.give(player == self.__players.getHumanPlayer()))
                if player == self.__players.getHumanPlayer():
                    player.sort()
                #TODO: DELAY_ANIM(100ms)

        self.__disc_deck.add(self.__buy_deck.give())

        while self.__disc_deck.topCard().value in SPECIAL_CARDS:
            self.__disc_deck.add(self.__buy_deck.give())
            #TODO: DELAY_ANIM(300ms)

        self.__state = 'PLAYER_TURN'


    def next_turn(self):
        self.__players.setNextTurn()
        self.players.already_buy = False
        if self.__players.turn == 0:
            self.__players.getCurrentPlayer().sort()
            self.__state = 'PLAYER_TURN'
        else:
            self.__state = 'BOT_TURN'

    def player_play_card(self, card_index):

        card:UnoCard = self.__players.getCurrentPlayer()[card_index]
        card.faceUp = True
        if self.__disc_deck.topCard().match(card):
            self.__disc_deck.add(self.__players.getCurrentPlayer().give(card))
            print(f'{self.__players.getCurrentPlayer().name}: played [{self.__disc_deck.topCard()}]')
            
            if self.__disc_deck.topCard().value in SPECIAL_CARDS:
                if self.__disc_deck.topCard().value in ['+4', 'wild']:
                    if self.__players.getCurrentPlayer() == self.__players.getHumanPlayer():
                        self.state = 'PLAYER_SELEC_COLOR'
                    else:
                        self.bot_select_color()
                if self.__disc_deck.topCard().value == '+2':
                    for i in range(2):
                        self.draw_card(self.__players.getNextPlayer())
                        #TODO: DELAY_ANIM(100ms)
                if self.__disc_deck.topCard().value in ['+2', 'block']:
                    self.__players.setNextTurn()
                if self.__disc_deck.topCard().value == 'reverse':
                    self.__players.flipRotation()
            if self.__players.getCurrentPlayer().isEmpty():
                self.state = 'ROUND_OVER'
            elif not self.__disc_deck.topCard().value in ['+4', 'wild']:
                self.next_turn()

    def human_select_color(self, color):
        if self.__disc_deck.topCard().color == '':
            self.__disc_deck.topCard().color = color
        if self.__disc_deck.topCard().value == '+4':
            for i in range(4):
                self.draw_card(self.__players.getNextPlayer())
                #TODO: DELAY_ANIM(100ms)
            self.__players.setNextTurn()
        self.next_turn()
    
    def bot_select_color(self):
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
                #TODO: DELAY_ANIM(100ms)
            self.__players.setNextTurn()
        self.next_turn()
                    
    def reshuffle_buy_deck(self):
        topCard = self.__disc_deck.give()
        topCard.flip()
        while not self.__disc_deck.isEmpty():
            if self.__disc_deck.topCard().value in ['+4', 'wild']:
                self.__disc_deck.topCard().color = ''
            self.__buy_deck.add(self.__disc_deck.give())
        self.__disc_deck.add(topCard)
        self.__buy_deck.shuffle()

    def draw_card(self, player):
        self.players.already_buy = True
        if self.__buy_deck.isEmpty():
            self.reshuffle_buy_deck()
        player.add(self.__buy_deck.give(player == self.__players.getHumanPlayer()))

    def player_draw_card(self, player):
        self.draw_card(player)
        for card in player:
            if card.match(self.__disc_deck.topCard()):
                return player.cards.index(card)
        else:
            self.next_turn()
        print(f'{player.name}: drew a card, ({self.__buy_deck.size()} cards left in the buy deck)')
        return -1

    def bot_play(self):
        for i, card in enumerate(self.__players.getCurrentPlayer().cards):
            if card.match(self.__disc_deck.topCard()):
                self.player_play_card(i)
                break
        else:
            print(f'{self.__players.getCurrentPlayer().name}: drew a card')
            buy_card_index = self.player_draw_card(self.__players.getCurrentPlayer())
            if buy_card_index != -1:
                self.player_play_card(buy_card_index)
        