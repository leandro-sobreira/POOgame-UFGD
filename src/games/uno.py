from src.classes.uno import UnoCard, UnoDeck, UnoHand, UnoPlayer

class UnoGame:
    def __init__(self):
        self.player = UnoPlayer('Lepanto')
        self.bot = UnoPlayer('Bot1')
        self.buyDeck = UnoDeck()
        self.discardDeck = UnoDeck()

    def botPlay(self, bot:UnoPlayer):
        for card in bot:
            if card.match(self.discardDeck.viewTop()):
                card:UnoCard = bot.give(card)
                self.discardDeck.add(card.flip())
                break
            else:
                bot.add(self.buyDeck.give())

    def playerPlay(self, player:UnoPlayer):

        print(f'Top card [{self.discardDeck.viewTop()}]')
        print(f'{self.bot.getName()}: ({self.bot.size()})')
        for i in range(player.size()):
            print(f'[{i+1}|{player[i]}] ', end='')
        print('')
        selec = input('Select card(0 to draw): ')
        if selec in range(1, player.size()):
            if player[i].match(self.discardDeck.viewTop()):
                self.discardDeck.add(player.give(player[i]))
            else:
                print('Incorrect value!')
                self.playerPlay(player)
        else:
            player.add(self.buyDeck.give())


    def play(self):
        self.buyDeck.createDeck()
        self.buyDeck.shuffle()
        for i in range(7):
            self.player.add(self.buyDeck.give())
            self.bot.add(self.buyDeck.give(False))
        self.discardDeck.add(self.buyDeck.give())
        #while self.discardDeck.viewTop().getValue() in ['+2', 'block', 'reverse', '+4', 'wild']:
        #    self.discardDeck.add(self.buyDeck.give())
        while not (self.player.isEmpty() and self.bot.isEmpty()):
            self.playerPlay(self.player)
            self.botPlay(self.bot)   
