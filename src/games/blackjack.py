from src.classes.standard import StandardDeck, StandardHand, StardardPlayer

class BlackjackGame:
    def __init__(self, player_name):
        self.player = StardardPlayer(player_name)
        self.table:StandardHand = StandardHand()
        self.gameDeck = StandardDeck()

    def play(self):

        reset = True
        while reset:
            print(f'{self.player.getName()}: {self.player.getPoints()}$')
            betAmount = int(input('Bet amount (min 10$)? '))
            if(betAmount < 10 or betAmount > self.player.getPoints()):
                print('Invalid vaule!')
            else:
                self.player.remPoints(betAmount)
                print(f'-{betAmount}$ ({self.player.getPoints()})')
                self.player.clear()
                self.table.clear()
                self.gameDeck.clear()
                self.gameDeck.createDeck()
                self.gameDeck.shuffle()
                self.table.add(self.gameDeck.give())
                self.player.add(self.gameDeck.give())
                self.table.add(self.gameDeck.give(False))
                self.player.add(self.gameDeck.give())
                opc = 'y'

                while True:
                    
                    if self.player.sumValues() < 21 and opc != 'n':
                        self.printCmd()
                        opc = input('Hit? [Y/N]: ').lower()
                        if opc == 'y':
                            self.player.add(self.gameDeck.give())
                    else:
                        self.table.flipAll(True)
                        self.printCmd()
                        input("Press Enter to continue")
                        while self.table.sumValues() < 17:
                            self.table.add(self.gameDeck.give())
                            self.printCmd()
                            input("Press Enter to continue")                   
                        break
                tableHandValue = self.table.sumValues()
                playerHandValue = self.player.sumValues()

                if(playerHandValue == tableHandValue or playerHandValue > 21 and tableHandValue > 21):
                    self.player.addPoints(betAmount)
                    print(f'{self.player.getName()} DRAW!! +{betAmount}$ ({self.player.getPoints()}$)')
                elif(playerHandValue > tableHandValue and playerHandValue <= 21 or tableHandValue > 21):
                    self.player.addPoints(betAmount*2)
                    print(f'{self.player.getName()} WIN!! +{betAmount*2}$ ({self.player.getPoints()}$)')
                else:
                    print(f'{self.player.getName()} LOSE! ({self.player.getPoints()}$)')

                if(self.player.getPoints() < 10):
                    print('Does not have the min points ;-;')
                    reset = False
                else:
                    reset = input("Again? ").lower() != 'n'


    def printCmd(self):
        print(f'Tabble: ({self.table.sumValues()})', end='')
        for card in self.table:
            print(f' [{card}]', end='')
        print('')
        print(f'{self.player.getName()}: ({self.player.sumValues()})', end='')
        for card in self.player:
            print(f' [{card}]', end='')
        print('')
