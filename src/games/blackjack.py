from classes.standard import StandardDeck, StandardHand, StardardPlayer
from src.interface import BlackjackScreen

class BlackjackGame:

    def __init__(self, player_name, screen):
        self.player = StardardPlayer(player_name)
        self.table:StandardHand = StandardHand()
        self.gameDeck = StandardDeck()
        self.tela = BlackjackScreen(screen)
        

    def play(self):

        reset = True
        
        while reset:

            self.player.clear()
            self.table.clear()
            self.gameDeck.clear()
            self.gameDeck.createDeck()
            self.gameDeck.shuffle()
            self.tela.loop(self.player.getCards(), self.table.getCards())
            print(f'{self.player.getName()}: {self.player.getPoints()}$')
            #betAmount = int(input('Bet amount (min 10$)? '))
            try:
                betAmount = int(self.tela.digitar('Bet amount (min 10$)?', True))
            except ValueError:
                print('Invalid input! Please enter a number.')
                continue
            print("retornado")
            print(int(betAmount))

            if(betAmount < 10 or betAmount > self.player.getPoints()):
                print('Invalid vaule!')
            else:
                self.player.remPoints(betAmount)
                print(f'-{betAmount}$ ({self.player.getPoints()})')

                self.table.add(self.gameDeck.give())
                self.tela.loop(self.player.getCards(), self.table.getCards(),300)
                self.player.add(self.gameDeck.give())
                self.tela.loop(self.player.getCards(), self.table.getCards(),300)
                self.table.add(self.gameDeck.give(False))
                self.tela.loop(self.player.getCards(), self.table.getCards(),300)
                self.player.add(self.gameDeck.give())
                self.tela.loop(self.player.getCards(), self.table.getCards(),300)
                opc = 'y'

                while True:

                    self.tela.loop(self.player.getCards(), self.table.getCards())
                    if self.player.sumValues() < 21 and opc != 'n':
                        self.printCmd()
                        #opc = input('Hit? [Y/N]: ').lower()
                        opc = self.tela.tecla()
                        print(opc)
                        if opc == 'y':
                            self.player.add(self.gameDeck.give())
                    else:
                        self.tela.loop(self.player.getCards(), self.table.getCards(),300)
                        self.table.flipAll(True)
                        self.tela.loop(self.player.getCards(), self.table.getCards(),300)
                        self.printCmd()
                        #input("Press Enter to continue")
                        #opc = self.tela.tecla()
                        while self.table.sumValues() < 17:
                            self.table.add(self.gameDeck.give())
                            self.tela.loop(self.player.getCards(), self.table.getCards(),750)
                            self.printCmd()
                            #input("Press Enter to continue") 
                            #opc = self.tela.tecla()                  
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
                    return -1
                else:

                    #reset = input("Again? [Y/N]: ").lower() != 'n'
                    reset = self.tela.digitar("Again? [Y/N]: ").lower() != 'n'

        return self.player.getPoints()


    def printCmd(self):
        print(f'Tabble: ({self.table.sumValues()})', end='')
        for card in self.table:
            print(f' [{card}]', end='')
        print('')
        print(f'{self.player.getName()}: ({self.player.sumValues()})', end='')
        for card in self.player:
            print(f' [{card}]', end='')
        print('')