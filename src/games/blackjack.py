from src.classes.standard import StandardDeck
from src.classes.deck import Deck
from src.classes.player import Player

# TEMPORARIO
def sumDeck(deck:Deck):
    tam = deck.getNumCards()
    scales = {'ace': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'jack': 10, 'queen': 10, 'king': 10}
    sum = 0
    ace = False
    for i in range(tam):
        if deck[i].getFace():
            if deck[i].getValue() == 'ace':
                ace = True
            sum += scales[deck[i].getValue()]
    if ace and sum < 12:
        sum += 10
    return sum

def printGame(tabble, player1):
    print(f'Tabble: ({sumDeck(tabble)})', end="")
    for i in range(tabble.getNumCards()):
        print(f' [{tabble[i]}]', end="")
    print('')
    print(f'Player: ({sumDeck(player1)})', end="")
    for i in range(player1.getNumCards()):
        print(f' [{player1[i]}]', end="")
    print('')

def game():
    reset = True
    while reset:
        gameDeck = StandardDeck()
        gameDeck.createDeck()
        gameDeck.suffle()
        player1 = Player('Lepanto', 1000)
        tabble = Deck()


        tabble + gameDeck.give()
        player1 + gameDeck.give()
        tabble + gameDeck.give(False)
        player1 + gameDeck.give()

        while True:
            printGame(tabble, player1)
            opc = input('Hit? [Y/N]: ')
            if opc == 'Y' or opc == 'y':
                player1 + gameDeck.give()
            else:
                tabble.flipAll(True)
                printGame(tabble, player1)
                input("Press Enter to continue")
                while(sumDeck(tabble) < 17):
                    tabble + gameDeck.give()
                printGame(tabble, player1)
                break

        reset = input("Again? ") == 'y'