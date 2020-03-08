import game.belot as belot
from game.interfaces import IPlayer

class PlayerKeyboard(IPlayer):

    def initialize(self):
        pass

    def notifyCards(self):
        pass

    def notifyTrumpSuit(self, trumpSuit, bidder):
        pass

    def notifyDeclarations(self, declarations):
        pass

    def notifyTrick(self, cards, value):
        pass

    def notifyHand(self, pointsUs, pointsThem):
        pass

    def notifyGame(self, pointsUs, pointsThem):
        pass

    def notifyBela(self, player, card):
        pass

    def bid(self, must):
        suits = list(belot.Suit)
        print("Cards: ", self.cards)
        while True:
            for i, suit in enumerate(suits):
                print("[{}] {}".format(i+1, suit), suit)

            choice = input("Color number (ENTER for further: ")
            if choice=="" and not must:
                return None

            try:
                choice = int(choice)
            except ValueError:
                continue

            if choice in range(1, len(suits)+1):
                break

        return suits[choice-1]

    def playCard(self, table, legalCards):
        print("Cards: ", self.cards)
        while True:
            for i, card in enumerate(legalCards):
                print("[{}] {}".format(i+1, card))

            choice = input("Ticket number:: ")

            try:
                choice = int(choice)
            except ValueError:
                continue

            if choice in range(1, len(legalCards)+1):
                break

        return legalCards[choice-1]

    def declareBela(self, table):
        while True:
            choice = input("Call it white (yes/no) ")
            if choice=="yes":
                return True
            elif choice=="no":
                return False

    def saveNetwork(self, number):
        pass
