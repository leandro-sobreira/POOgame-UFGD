from src.classes.standard import StandardDeck, StandardHand, StardardPlayer

class blackjackGame:
    def __init__(self, player_name):
        self.player = StardardPlayer(player_name)
        self.table:StandardHand = StandardHand()
        self.gameDeck = StandardDeck()
        self.discardDeck = StandardDeck()

        self.gameDeck.createDeck()
        self.gameDeck.shuffle()

    def play(self):
        reset = True
        while reset:
            self.table.add(self.gameDeck.give())
            self.player.add(self.gameDeck.give())
            self.table.add(self.gameDeck.give(False))
            self.player.add(self.gameDeck.give())

            while True:
                self.printCmd()
                opc = input('Hit? [Y/N]: ')
                if opc == 'Y' or opc == 'y':
                    self.player.add(self.gameDeck.give())
                else:
                    self.table.flipAll(True)
                    self.printCmd()
                    input("Press Enter to continue")
                    while self.table.sumValues() < 17:
                        self.table.add(self.gameDeck.give())
                    self.printCmd()
                    break

            reset = input("Again? ") == 'y'


    def printCmd(self):
        print(f'Tabble: ({self.table.sumValues()})', end='')
        for card in self.table:
            print(f' [{card}]', end='')
        print('')
        print(f'{self.player.getName()}: ({self.player.sumValues()})', end='')
        for card in self.player:
            print(f' [{card}]', end='')
        print('')
