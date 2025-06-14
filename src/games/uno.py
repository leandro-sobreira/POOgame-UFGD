from ..classes.uno import UnoDeck, UnoPlayer, UnoPlayers, UnoCard
import random

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
    def getPlayers(self):
        return self.__players
    def getBuyDeck(self):
        return self.__buy_deck
    def getDiscDeck(self):
        return self.__disc_deck
    def getState(self):
        return self.__state
    
    def setState(self, state:str):
        self.__state = state

    def start_round(self):
        self.__disc_deck.clear()
        self.__buy_deck.clear()
        self.__players.clear()
        self.__buy_deck.createDeck()
        self.__buy_deck.shuffle()
        for i in range(7):
            for player in self.__players:
                player.add(self.__buy_deck.give(player == self.__players.getHumanPlayer()))
                if player == self.__players.getHumanPlayer():
                    player.sort()
                #TODO: DELAY_ANIM(100ms)
        self.__disc_deck.add(self.__buy_deck.give())
        while self.__disc_deck.topCard().getValue() in SPECIAL_CARDS:
            self.__disc_deck.add(self.__buy_deck.give())
            #TODO: DELAY_ANIM(300ms)
        self.setState('PLAYER_TURN')


    def next_turn(self):
        self.__players.setNextTurn()
        if self.__players.getTurn() == 0:
            self.__players.getCurrentPlayer().sort()
            self.setState('PLAYER_TURN')
        else:
            self.setState('BOT_TURN')


    def player_play_card(self, card_index):

        card:UnoCard = self.__players.getCurrentPlayer()[card_index]
        card.setFaceUp(True)
        if self.__disc_deck.topCard().match(card):
            self.__disc_deck.add(self.__players.getCurrentPlayer().give(card))
            print(f'{self.__players.getCurrentPlayer().getName()}: played [{self.__disc_deck.topCard()}]')
            
            if self.__disc_deck.topCard().getValue() in SPECIAL_CARDS:
                if self.__disc_deck.topCard().getValue() in ['+4', 'wild']:
                    if self.__players.getCurrentPlayer() == self.__players.getHumanPlayer():
                        self.setState('PLAYER_SELEC_COLOR')
                    else:
                        self.bot_select_color()
                if self.__disc_deck.topCard().getValue() == '+2':
                    for i in range(2):
                        self.__players.getNextPlayer().add(self.__buy_deck.give(self.__players.getNextPlayer() == self.__players.getHumanPlayer()))
                        #TODO: DELAY_ANIM(100ms)
                if self.__disc_deck.topCard().getValue() in ['+2', 'block']:
                    self.__players.setNextTurn()
                if self.__disc_deck.topCard().getValue() == 'reverse':
                    self.__players.flipRotation()
            if self.__players.getCurrentPlayer().isEmpty():
                self.setState('ROUND_OVER')
            elif not self.__disc_deck.topCard().getValue() in ['+4', 'wild']:
                self.next_turn()

    #QUANDO O BOTÃO DA COR É SELECIONADO RETORNA ESSA COR PARA ESSA FUNÇÃO
    def human_select_color(self, color):
        if self.__disc_deck.topCard().getColor() == '':
            self.__disc_deck.topCard().setColor(color)
        if self.__disc_deck.topCard().getValue() == '+4':
            for i in range(4):
                self.__players.getNextPlayer().add(self.__buy_deck.give(self.__players.getNextPlayer() == self.__players.getHumanPlayer()))
                #TODO: DELAY_ANIM(100ms)
            self.__players.setNextTurn()
        self.next_turn()
    
    def bot_select_color(self):
        if self.__disc_deck.topCard().getColor() == '':
            for card in self.__players.getCurrentPlayer():
                if card.getColor() != '':
                    self.__disc_deck.topCard().setColor(card.getColor())
                    break
            else:
                self.__disc_deck.topCard().setColor(random.choice(UNO_COLORS))
        if self.__disc_deck.topCard().getValue() == '+4':
            for i in range(4):
                self.__players.getNextPlayer().add(self.__buy_deck.give(self.__players.getNextPlayer() == self.__players.getHumanPlayer()))
                #TODO: DELAY_ANIM(100ms)
            self.__players.setNextTurn()
        self.next_turn()
                    
    def reshuffle_buy_deck(self):
        #TODO: RESHUFFLE_ANIM
        topCard = self.__disc_deck.give()
        topCard.flip()
        while not self.__disc_deck.isEmpty():
            if self.__disc_deck.topCard().getValue() in ['+4', 'wild']:
                self.__disc_deck.topCard().setColor('')
            self.__buy_deck.add(self.__disc_deck.give())
        self.__disc_deck.add(topCard)
        self.__buy_deck.shuffle()

    def human_draw_card(self):
        if self.__buy_deck.isEmpty():
            self.reshuffle_buy_deck()
        self.__players.getCurrentPlayer().add(self.__buy_deck.give())
        self.__players.getCurrentPlayer().sort()
        #TODO: DELAY_ANIM(100ms)
        self.next_turn()

    def bot_draw_card(self):
        if self.__buy_deck.isEmpty():
            self.reshuffle_buy_deck()
        card = self.__buy_deck.give(False)
        self.__players.getCurrentPlayer().add(card)
        if self.__disc_deck.topCard().match(card):
            self.player_play_card(self.__players.getCurrentPlayer().getCards().index(card))
            #TODO: DELAY_ANIM(100ms)
        self.next_turn()

    def bot_play(self):
        #TODO: BOT_THINKING_ANIM
        for i, card in enumerate(self.__players.getCurrentPlayer().getCards()):
            if card.match(self.__disc_deck.topCard()):
                self.player_play_card(i)
                break
        else:
            print(f'{self.__players.getCurrentPlayer().getName()}: drew a card')
            self.bot_draw_card()
        