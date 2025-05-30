from src.classes.standard import StandardDeck, StandardCard, StandardHand
from src.classes.player import Player

def getCardValue(card:StandardCard):
    return card.getValue()

def printGame(tabble, player1):
    print(f'Tabble: ({tabble.sumValues()})', end="")
    for card in tabble.getCards():
        print(f' [{card}]', end="")
    print('')
    print(f'Player: ({player1().getHand().sumValues()})', end="")
    for card in player1.getHand().getCards():
        print(f' [{card}]', end="")
    print('')

def game():
    reset = True
    while reset:
        gameDeck = StandardDeck()
        gameDeck.createDeck()
        gameDeck.suffle()
        player1 = Player('Lepanto', 1000, StandardHand())
        tabble = StandardHand()

        tabble.add(gameDeck.give())
        player1._hand.add(gameDeck.give())
        tabble.add(gameDeck.give().flip())
        player1._hand.add(gameDeck.give())

        while True:
            printGame(tabble, player1)
            opc = input('Hit? [Y/N]: ')
            if opc == 'Y' or opc == 'y':
                player1 += gameDeck.give()
            else:
                tabble.flipAll(True)
                printGame(tabble, player1)
                input("Press Enter to continue")
                #while sumDeck(tabble) < 17:
                #    tabble += gameDeck.give()
                #printGame(tabble, player1)
                break

        reset = input("Again? ") == 'y'