import os
import random
from ..classes.uno import UnoCard, UnoDeck, UnoPlayer, UnoPlayers

class UnoGame:
    def __init__(self, playersName = []):
        self.players = UnoPlayers(playersName)
        self.buyDeck = UnoDeck()
        self.discardDeck = UnoDeck()
        self.specialCards = ['+2', 'block', 'reverse', '+4', 'wild']
                
    def reshuffleBuyDeck(self):
        if self.buyDeck.isEmpty():
            print('Reshuffling buy deck...')
            topCard:UnoCard = self.discardDeck.give() #Guarda a carta do topo do baralho de descarte
            if topCard.getValue() in ['+4', 'wild']: #Se a carta do topo for um +4 ou wild, remove a cor dela
                topCard.setColor('')
            topCard.flip() 
            while not self.discardDeck.isEmpty(): #Passa as cartas do baralho de descarte para o baralho de compra uma por uma
                if self.discardDeck.viewTop().getValue() in ['+4', 'wild']: #Se a carta do topo for um +4 ou wild, remove a cor dela
                    self.discardDeck.viewTop().setColor('')
                self.buyDeck.add(self.discardDeck.give())
            self.discardDeck.add(topCard) #Adiciona a carta do topo do baralho de descarte de volta ao baralho de descarte
            self.buyDeck.shuffle() #Embaralha o baralho de compra

    def buyCard(self, player):
        if self.buyDeck.isEmpty(): #Se o baralho de compra estiver vazio, embaralha o baralho de descarte
            self.reshuffleBuyDeck()
        player.add(self.buyDeck.give())

    def playCard(self,player:UnoPlayer, card:UnoCard):
        if not self.discardDeck.viewTop().match(card): #Verifica se a carta jogada combina com a carta do topo do baralho de descarte
            raise ValueError('Card does not match the top of the discard deck!')
        else:
            if card.getValue() in self.specialCards: #Se a carta for uma carta especial, executa as ações correspondentes
                if card.getColor() == '': #Se a carta não tiver cor, pede ao jogador para escolher uma cor
                    while True:
                        color = input('Select a color [red, yellow, green, blue]: ').lower()
                        if color in ['red', 'yellow', 'green', 'blue']:
                            card.setColor(color)
                            break
                        else:
                            print('Invalid color selected!')
                if card.getValue() in ['+2', '+4']: #Se a carta for um +2 ou +4, o próximo jogador compra as cartas correspondentes
                    for i in range(int(card.getValue())): 
                        self.buyCard(self.players.getNextPlayer())
                if card.getValue() in ['+2', '+4', 'block']: #Se a carta for um +2, +4 ou block, o próximo jogador não joga
                    self.players.setNextTurn()
                if card.getValue() == 'reverse': #Se a carta for um reverse, inverte a ordem dos jogadores
                    self.players.flipRotation()
            self.discardDeck.add(player.give(card)) #Adiciona a carta jogada ao baralho de descarte

    def playerPlay(self, player:UnoPlayer):
        if self.players.getRotation() == 1:
            end = ' -> '
        else:
            end = ' <- '
        for plyer in self.players:
            print(f'{plyer.getName()}: ({plyer.size()})', end=end)
        print('')
        print(f'{player.getName()}\'s turn')
        player.sort()
        print(f'Discard deck top: [{self.discardDeck.viewTop()}]')
        i = 1
        for card in player:
            print(f'{i}-[{card}] ',end='')
            i += 1
        print('')
        
        while True:
            try:
                selec = int(input("Selec a card or 0 to draw: "))-1
                if selec == -1:
                    self.buyCard(player)
                    if player.getCards()[-1].match(self.discardDeck.viewTop()):
                        opc = input(f'Do you want to play the card you just drew [{player.getCards()[-1]}]? [Y/N]: ').lower()
                        if opc == 'y':
                            self.playCard(player, player.getCards()[-1])
                else:
                    self.playCard(player, player[selec])
                break
            
            except ValueError:
                print('Invalid input! Please enter a number.')
                continue
            except IndexError:
                print('Invalid selection! Please select a valid card number or 0.')
                continue
        print('-----------------------------------------------------')

    def botPlayCard(self, bot:UnoPlayer, playCard:UnoCard):
        if playCard.getValue() in self.specialCards:
                if playCard.getColor() == '':
                    for card in bot.getCards():
                        if card.getColor() != '': 
                            playCard.setColor(card.getColor())
                            break
                    else:
                        playCard.setColor(random.choice(['red', 'yellow', 'green', 'blue']))
                if playCard.getValue() in ['+2', '+4']:
                    for i in range(int(playCard.getValue())):
                        self.buyCard(self.players.getNextPlayer())
                if playCard.getValue() in ['+2', '+4', 'block']:
                    print(f'{bot.getName()}: played [{playCard}] in {self.players.getNextPlayer().getName()}')
                    self.players.setNextTurn()
                else:
                    print(f'{bot.getName()}: played [{playCard}]')
                if playCard.getValue() == 'reverse':
                    self.players.flipRotation()
        else:
            print(f'{bot.getName()}: played [{playCard}]')
        self.discardDeck.add(bot.give(playCard))

    def botPlay(self, bot:UnoPlayer):
        random.shuffle(bot.getCards())
        for card in bot:
            if card.match(self.discardDeck.viewTop()):
                self.botPlayCard(bot, card)
                break
        else:
            self.buyCard(bot)
            print(f'{bot.getName()}: drew a card')
            if bot.getCards()[-1].match(self.discardDeck.viewTop()):
                self.botPlayCard(bot,bot.getCards()[-1])

    def play(self):
        #Inicializa o jogo
        self.buyDeck.createDeck()
        self.buyDeck.shuffle()
        for i in range(7):
            for player in self.players:
                player.add(self.buyDeck.give())
        self.discardDeck.add(self.buyDeck.give())
        while self.discardDeck.viewTop().getValue() in self.specialCards: #Não permite que a primeira carta do baralho de descarte seja uma carta especial
            self.discardDeck.add(self.buyDeck.give())
        
        os.system('cls' if os.name == 'nt' else 'clear')
        while (True):
            if self.players.getCurrentPlayer().getName().startswith('Bot'):
                self.botPlay(self.players.getCurrentPlayer())
            else:
                self.playerPlay(self.players.getCurrentPlayer())
            
            if self.players.getCurrentPlayer().isEmpty():
                break #Se o jogador que acabou de jogar ficar sem cartas termina o jogo;
            self.players.setNextTurn()#Passa a vez do jogador
        for player in self.players:
            if not player == self.players.getCurrentPlayer():
                self.players.getCurrentPlayer().addPoints(player.sumValues()) #Adiciona os pontos das cartas dos outros jogadores ao jogador que ganhou
        
        print(f'{self.players.getCurrentPlayer().getName()}: WIN! {self.players.getCurrentPlayer().getPoints()} points')
        return self.players.getTurn()