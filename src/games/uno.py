import os
import random
from src.classes.uno import UnoCard, UnoDeck, UnoPlayer

class UnoGame:
    def __init__(self, playersName = []):
        self.players = []
        for playerName in playersName:
            self.players.append(UnoPlayer(playerName))
        self.playerTurn = 0
        self.rotation = 1
        self.buyDeck = UnoDeck()
        self.discardDeck = UnoDeck()
        self.specialCards = ['+2', 'block', 'reverse', '+4', 'wild']
                
    def reshuffleBuyDeck(self):
        if self.buyDeck.isEmpty():
            print('Reshuffling buy deck...')
            topCard:UnoCard = self.discardDeck.give()
            if topCard.getValue() in ['+4', 'wild']:
                topCard.setColor('')
            topCard.flip() 
            while not self.discardDeck.isEmpty():
                if self.discardDeck.viewTop().getValue() in ['+4', 'wild']:
                    self.discardDeck.viewTop().setColor('')
                self.buyDeck.add(self.discardDeck.give())
            self.discardDeck.clear()
            self.discardDeck.add(topCard)
            self.buyDeck.shuffle()

    def buyCard(self, player):
        if self.buyDeck.isEmpty():
            self.reshuffleBuyDeck()
        player.add(self.buyDeck.give())

    def playCard(self, player:UnoPlayer, card:UnoCard):
        if card.match(self.discardDeck.viewTop()): #Ve se a carta é valida
            if card.getValue() in self.specialCards: #Se a carta é valida, ve se a carta é especial
                if card.getColor() == '': #Se for uma carta preta, faz a seleção de cor
                    color = input('Select color [red, yellow, green, blue]: ').lower()
                    while color not in ('red', 'yellow', 'green', 'blue'):
                        print('Invalid color!')
                        color = input('Select color [red, yellow, green, blue]: ').lower()
                    card.setColor(color)
                if card.getValue() == 'reverse': #Se a carta é um reverse muda a rotação do jogo
                    self.rotation = self.rotation * -1
                if card.getValue() in ['+2', '+4']:#Se for uma carta de compra, o proximo player compra a quantidade da carta
                    for i in range(int(card.getValue())):#Transforma o texto '+4' e '+2' nos numeros 4 e 2 respectivamente
                        self.buyCard(self.players[(self.playerTurn+self.rotation)%len(self.players)])
                if card.getValue() in ['+2', 'block', '+4']:#Se a carta for um bloqueio ou uma carta de compra, pula o proximo player
                    self.playerTurn = (self.playerTurn+self.rotation)%len(self.players)
            self.discardDeck.add(player.give(card))#Descarta a carta no baralho de descarte
        else:
            print('Invalid card!')
            self.playerPlay(player)#Se a carta selecionada não é valida, faz uma nova requisição de jogada

                    
    def playerPlay(self, player:UnoPlayer):
        player.sort()
        print(f'Top card [{self.discardDeck.viewTop()}]')
        for othersPlayres in self.players:
            if(self.rotation == 1):
                end = ' -> '
            else:
                end = ' <- '
            if othersPlayres == player:
                print(f'{othersPlayres.getName()}: (you)', end=end)
            else:
                print(f'{othersPlayres.getName()}: ({othersPlayres.size()})', end=end)
        print('')
        for i in range(player.size()):
            print(f'[{i+1}|{player[i]}] ', end='')
        print('')
        while True:
            try: 
                selec = int(input('Select card(0 to draw): '))-1 #Tenta denovo até ter uma opção válida
                break
            except ValueError:
                print('Incorrect value! Please enter a number.')
        if not selec == -1: #Ve se o player não selecionou a opção de comprar carta
            self.playCard(player, player[selec]) #Joga uma carta
        else:
            self.buyCard(player) #Compra uma carta
            if player.getCards()[-1].match(self.discardDeck.viewTop()): #Ve se a carta comprada pode ser jogada
                opc = input(f'Do you want to play the card you just drew [{player.getCards()[-1]}]? [Y/N]: ').lower() #Pergunta para o jogador se ele quer jogar a carta comprada
                if opc == 'y':
                    self.playCard(player, player.getCards()[-1])
        os.system('cls' if os.name == 'nt' else 'clear')

    def botPlayCard(self, bot:UnoPlayer, playCard:UnoCard):
        if playCard.getValue() in self.specialCards: #Se a carta é valida, ve se a carta é especial
            if playCard.getColor() == '': #Se for uma carta preta, faz a seleção de cor
                for card in bot.getCards(): #Tenta encontrar uma carta que tenha cor para selecionar esse cor
                    if card.getColor() != '': 
                        playCard.setColor(card.getColor())
                        break
                else:
                    playCard.setColor(random.choice(['red', 'yellow', 'green', 'blue'])) #Se não tiver nenhuma carta com cor, escolhe uma cor aleatória
            if playCard.getValue() == 'reverse': #Se a carta é um reverse muda a rotação do jogo
                self.rotation = self.rotation * -1
            if playCard.getValue() in ['+2', '+4']:#Se for uma carta de compra, o proximo player compra a quantidade da carta
                for i in range(int(playCard.getValue())):#Transforma o texto '+4' e '+2' nos numeros 4 e 2 respectivamente
                    self.buyCard(self.players[(self.playerTurn+self.rotation)%len(self.players)])
            if playCard.getValue() in ['+2', 'block', '+4']:#Se a carta for um bloqueio ou uma carta de compra, pula o proximo player
                self.playerTurn = (self.playerTurn+self.rotation)%len(self.players)
        print(f'{bot.getName()}: played [{playCard}]')
        self.discardDeck.add(bot.give(playCard))#Descarta a carta no baralho de descarte

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
            if self.players[self.playerTurn].getName().startswith('Bot'):
                self.botPlay(self.players[self.playerTurn])
            else:
                self.playerPlay(self.players[self.playerTurn])
            
            if self.players[self.playerTurn].isEmpty():
                break #Se o jogador que acabou de jogar ficar sem cartas termina o jogo;
            self.playerTurn = (self.playerTurn+self.rotation)%len(self.players) #Passa a vez do jogador
        
        print(f'{self.players[self.playerTurn].getName()}: WIN!')
        return self.playerTurn

