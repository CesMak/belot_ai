import game.belot as belot
from players.PlayerKeyboard import PlayerKeyboard


class Pair:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

        self.iter=-1

    def __eq__(self, other):
        if other==None:
            return False

        return self.player1 == other.player1 and self.player2 == other.player2

    def __str__(self):
        return "{} i {}".format(self.player1, self.player2)

    def __repr__(self):
        return self.__str__()

    def __contains__(self, other):
        return other == self.player1 or other == self.player2

    def __iter__(self):
        self.iter = -1
        return self

    def __next__(self):
        self.iter += 1

        if self.iter == 0:
            return self.player1
        elif self.iter == 1:
            return self.player2
        elif self.iter >= 2:
            raise StopIteration


class Hand:
    def __init__(self, game):
        self.game = game

        # tuple-style tricks (card1, card2, card3, card4)
        self.tricksA = list()
        self.tricksB = list()

        self.pointsA = 0 # points accumulated A
        self.pointsB = 0 # skupljeni bodovi para B

        self.declarations = dict()

        # player mapping to the index
        self.sittingIndices = dict()
        for i, player in enumerate(game.sitting):
            self.sittingIndices[player]=i

        #a table to build a local 'table' of status that is handed over to the agent
        self.mapTableToLocal = dict()
        for player in self.game.sitting:
            self.mapTableToLocal[player]=dict()
            self.setCurrentPlayer(player)
            self.mapTableToLocal[player][player]=belot.PlayerRole.ME
            self.mapTableToLocal[player][self.whoWasPreviousPlayer()]=belot.PlayerRole.LEFT_OPPONENT
            self.mapTableToLocal[player][self.whoIsNextPlayer()]=belot.PlayerRole.RIGHT_OPPONENT
            self.mapTableToLocal[player][self.getTeammate(player)]=belot.PlayerRole.TEAMMATE

        self.currentPlayer=None
        self.resetToFirstPlayer()

    def resetToFirstPlayer(self):
        self.playerIndex=self.game.dealerIndex
        self.nextPlayer()

    def setCurrentPlayer(self, player):
        self.playerIndex=self.sittingIndices[player]
        self.currentPlayer=player

    def previousIndex(self):
        return (self.playerIndex-1)%4

    def whoWasPreviousPlayer(self):
        return self.game.sitting[self.previousIndex()]

    def nextIndex(self):
        return (self.playerIndex+1)%4

    def whoIsNextPlayer(self):
        return self.game.sitting[self.nextIndex()]

    def nextPlayer(self):
        self.currentPlayer=self.whoIsNextPlayer()
        self.playerIndex=self.nextIndex()

    def getTeammate(self, player):
        if player in self.game.pairA:
            for p in self.game.pairA:
                if p!=player:
                    return p
        elif player in self.game.pairB:
            for p in self.game.pairB:
                if p!=player:
                    return p

    def updatePlayersCards(self, cards1, cards2, cards3, cards4):
        self.game.sitting[0].updateCards(cards1)
        self.game.sitting[1].updateCards(cards2)
        self.game.sitting[2].updateCards(cards3)
        self.game.sitting[3].updateCards(cards4)

    def play(self):

        print("Card dealer: {}".format(self.game.sitting[self.game.dealerIndex]))
        pairA = self.game.pairA
        pairB = self.game.pairB
        playerA1 = pairA.player1
        playerA2 = pairA.player2
        playerB1 = pairB.player1
        playerB2 = pairB.player2
        #Hand 8 cards
        cards1, cards2, cards3, cards4 = belot.dealCards()

        # uruči igračima prvih 6 karata za zvanje aduta
        # hands players the first 6 cards to be called trump card
        self.updatePlayersCards(cards1[:-2], cards2[:-2], cards3[:-2], cards4[:-2])

        # zvanje aduta
        #the title of trump card
        biddingPair=None
        while True:
            print("---------- {} ----------".format(self.currentPlayer))
            must = (self.playerIndex == self.game.dealerIndex)
            print("must", must)
            suit = self.currentPlayer.bid(must=must)
            #print("suit", suit, "belot.Suit", belot.Suit)
            if suit in belot.Suit:
                print("{} calling {}".format(self.currentPlayer, suit), suit)
                if self.currentPlayer in pairA: biddingPair=pairA
                elif self.currentPlayer in pairB: biddingPair=pairB
                trumpSuit = suit
                bidder = self.currentPlayer
                break
            else:
                if must: raise ValueError("{} he didn't call for us!".format(self.currentPlayer))

                print("Player", self.currentPlayer, "says further")
            self.nextPlayer()
        print("Bidding Pair:", biddingPair, "Bidder:", bidder)

        for player in self.game.sitting:
            localBidder = self.mapTableToLocal[player][bidder]
            player.notifyTrumpSuit(trumpSuit, localBidder)

        #plays the first player to the right of the dealer
        self.resetToFirstPlayer() # igra prvi igrač desno od djelitelja

        # uruči igračima sve karte
        #hand players all the cards (not just 6 but 8)
        print("Handing now all 8 cards:")
        self.updatePlayersCards(cards1, cards2, cards3, cards4)

        # zvanja
        # vocations
        print(">>>>>>>>Declaring Phase <<<<<<<<<<<<<<<<<<<")
        declaredCardsA1, declaredValuesA1 = playerA1.declare()
        declaredCardsA2, declaredValuesA2 = playerA2.declare()
        maxDeclaredA1 = max(declaredValuesA1) if len(declaredValuesA1)!=0 else 0
        maxDeclaredA2 = max(declaredValuesA2) if len(declaredValuesA2)!=0 else 0
        maxDeclaredA = max([maxDeclaredA1, maxDeclaredA2])

        declaredCardsB1, declaredValuesB1 = playerB1.declare()
        declaredCardsB2, declaredValuesB2 = playerB2.declare()
        maxDeclaredB1 = max(declaredValuesB1) if len(declaredValuesB1)!=0 else 0
        maxDeclaredB2 = max(declaredValuesB2) if len(declaredValuesB2)!=0 else 0
        maxDeclaredB = max([maxDeclaredB1, maxDeclaredB2])

        declareA = False
        declareB = False

        # belot ?
        belotValue = 1001
        belotPlayer = None

        if belotValue in declaredValuesA1:
            belotPlayer = playerA1
        elif belotValue in declaredValuesA2:
            belotPlayer = playerA2
        elif belotValue in declaredValuesB1:
            belotPlayer = playerB1
        elif belotValue in declaredValuesB1:
            belotPlayer = playerB1

        print("Test if a player has belot", belotValue, )
        print("maxDeclaredA", maxDeclaredA)
        print("maxDeclaredB", maxDeclaredB)

        if belotPlayer is not None:
            print("{} there is belot!".format(belotPlayer))
            if belotPlayer in pairA:
                return belotValue, 0
            elif belotPlayer in pairB:
                return 0, belotValue

        print("Depending on maxDeclaredA, maxDeclared B - vocations:")
        if maxDeclaredA==0 and maxDeclaredB==0:
            print("\t No vocation")
        elif maxDeclaredA>maxDeclaredB:
            declareA=True
        elif maxDeclaredA<maxDeclaredB:
            declareB=True
        else:
            nextPlayer = self.whoIsNextPlayer()
            if nextPlayer in pairA:
                declareA=True
            elif nextPlayer in pairB:
                declareB=True

        handValue = belot.handValue
        print("belot.handValue", belot.handValue)
        print("declareA", declareA, "declareB", declareB)
        if declareA:
            declarationsTotalA=sum(declaredValuesA1+declaredValuesA2)
            handValue+=declarationsTotalA
            self.pointsA+=declarationsTotalA
            if len(declaredCardsA1)!=0:

                self.declarations[playerA1]=declaredCardsA1
                print("\tDeclarations {}: {}".format(playerA1, declaredCardsA1))
            if len(declaredCardsA2)!=0:
                self.declarations[playerA2]=declaredCardsA2
                print("\ttDeclarations {}: {}".format(playerA2, declaredCardsA2))
        elif declareB:
            declarationsTotalB=sum(declaredValuesB1+declaredValuesB2)
            handValue+=declarationsTotalB
            self.pointsB+=declarationsTotalB
            if len(declaredCardsB1)!=0:
                self.declarations[playerB1]=declaredCardsB1
                print("\ttDeclarations {}: {}".format(playerB1, declaredCardsB1))
            if len(declaredCardsB2)!=0:
                self.declarations[playerB2]=declaredCardsB2
                print("\ttDeclarations {}: {}".format(playerB2, declaredCardsB2))

        print("Local Declarations")
        for player in self.game.sitting:
            localDeclarations=dict()
            for playerKey in self.declarations:
                declaredCards = self.declarations[playerKey]
                localKey = self.mapTableToLocal[player][playerKey]
                localDeclarations[localKey]=declaredCards
            print(localDeclarations)
            player.notifyDeclarations(localDeclarations)

        # započni igru
        # start the game
        print(">>>>>>>>Playing Phase <<<<<<<<<<<<<<<<<<<")
        while len(self.tricksA) + len(self.tricksB) < 8:
            if self.game.humanPlayer: input()

            trick=list() # Stich
            table=dict() # cards on the table karte na stolu
            lastTrick = (len(self.tricksA)+len(self.tricksB) == 7)
            dominantSuit=None

            while len(table)<4:
                print("\n", "---------- {} ----------".format(self.currentPlayer))

                localTable=dict()
                for player in table:
                    card = table[player]
                    localKey = self.mapTableToLocal[self.currentPlayer][player]
                    localTable[localKey]=card

                playerLegalCards = belot.getLegalCards(self.currentPlayer.cards, table, dominantSuit, trumpSuit)
                print("localTable", localTable)
                card = self.currentPlayer.playCard(localTable, playerLegalCards)
                if card not in playerLegalCards:
                    raise ValueError("{} has thrown a card he cannot throw!".format(self.currentPlayer))

                self.currentPlayer.cards.remove(card)

                suit, rank = card
                if suit == trumpSuit:
                    queenAndKing = (rank == belot.Rank.DAMA and belot.Card(suit, belot.Rank.KRALJ) in self.currentPlayer.cards)
                    kingAndQueen = (rank == belot.Rank.KRALJ and belot.Card(suit, belot.Rank.DAMA) in self.currentPlayer.cards)
                    if (queenAndKing or kingAndQueen) and self.currentPlayer.declareBela(localTable):
                        print("BEAUTIFUL!")
                        handValue+=belot.belaValue
                        if self.currentPlayer in pairA:
                            self.pointsA+=belot.belaValue
                        elif self.currentPlayer in pairB:
                            self.pointsB+=belot.belaValue

                        for player in self.game.sitting:
                            if player!=self.currentPlayer:
                                player.notifyBela(self.currentPlayer, card)
                print(card)

                if dominantSuit==None:
                    dominantSuit = suit

                table[self.currentPlayer]=card
                trick.append(card)

                self.nextPlayer()

            trickWinner = belot.trickWinner(table, dominantSuit, trumpSuit)
            trickValue = belot.trickValue(table, trumpSuit, lastTrick)
            print("> Stich ({}) made by {}".format(trickValue, trickWinner))

            print(">>>>>>>>End of one Round<<<<<<<<<<<<<<<<<<<")
            if trickWinner in pairA:
                self.tricksA.append(tuple(trick))
                self.pointsA+=trickValue
                print("TRICK:", trick)
                print("trickValue", trickValue)
                for playerA in pairA:
                    playerA.notifyTrick(trick, trickValue)
                for playerB in pairB:
                    playerB.notifyTrick(trick, -trickValue)

            elif trickWinner in pairB:
                self.tricksB.append(tuple(trick))
                self.pointsB+=trickValue
                for playerA in pairA:
                    playerA.notifyTrick(trick, -trickValue)
                for playerB in pairB:
                    playerB.notifyTrick(trick, trickValue)

            self.setCurrentPlayer(trickWinner)

        # Alle stiche gemacht?
        stihMac = False
        if len(self.tricksA) == 8:
            print("{} they made all stiche (sword)".format(pairA))
            self.pointsA += belot.stihMacValue + self.pointsB
            self.pointsB = 0
            stihMac = True
        elif len(self.tricksB) == 8:
            print("{} they made all stiche (sword)!".format(pairB))
            self.pointsB += belot.stihMacValue + self.pointsA
            self.pointsA = 0
            stihMac = True

        if stihMac:
            return self.pointsA, self.pointsB

        print("Sharing Points:")
        print("\t{}: {}".format(pairA, self.pointsA))
        print("\t{}: {}".format(pairB, self.pointsB))

        # Passing or not passing prolaz ?
        print("Check passing, if points.A < handValue //2+1", "HandValue(=belot.handValue=162+maxDeclared)", handValue, handValue//2+1)
        if biddingPair == pairA and self.pointsA < handValue // 2 + 1:
                print("{} they did not pass!".format(pairA))
                self.pointsB += self.pointsA
                self.pointsA = 0
        elif biddingPair == pairB and self.pointsB < handValue // 2 + 1:
                print("{} they did not pass!".format(pairB))
                self.pointsA += self.pointsB
                self.pointsB = 0

        return self.pointsA, self.pointsB


class Game:
    '''
    Razred koji predstavlja igru dva protivnička para do 1001 bod
    A class that represents the game of two opposing pairs up to 1001 points
    '''

    def __init__(self, pairA, pairB):
        self.pairA = pairA
        self.pairB = pairB

        # ukupni bodovi kroz sva dijeljenja
        #total points across all divisions
        self.pointsA = 0
        self.pointsB = 0

        self.sitting = [pairA.player1, pairB.player1, pairA.player2, pairB.player2]
        self.dealerIndex = 0

        self.humanPlayer=False
        # osiguraj da svi igrači imaju različita imena
        # ensure that all players have different names
        for i in range(len(self.sitting)):
            player = self.sitting[i]

            if player.human:
                self.humanPlayer=True

            if player in self.sitting[i+1:]:
                raise ValueError("There cannot be two players with the same name ({})!".format(player))

    def nextDealer(self):
        self.dealerIndex=(self.dealerIndex+1)%4

    def play(self):
        winA=False
        winB=False

        print("PAIR A:",  self.pairA)
        print("PAIR B::", self.pairB, "\n")

        while True:
            if self.humanPlayer: input()
            print("================= SHARING =================")
            hand = Hand(self) # go to class hand(gameobject)
            newPointsA, newPointsB = hand.play()

            print("One Game finished, Update the Policy for", "newPointsA", newPointsA, "newPointsB", newPointsB)
            for playerA in self.pairA:
                playerA.notifyHand(newPointsA, newPointsB)
            for playerB in self.pairB:
                playerB.notifyHand(newPointsB, newPointsA)

            self.nextDealer()

            self.pointsA+=newPointsA
            self.pointsB+=newPointsB
            print("Total points:")
            print("\t{}: {}".format(self.pairA, self.pointsA))
            print("\t{}: {}".format(self.pairB, self.pointsB))

            if self.pointsA>=1001 and self.pointsB>=1001:
                if self.pointsA>self.pointsB:
                    winA=True
                elif self.pointsA<self.pointsB:
                    winB=True
                break
            elif self.pointsA>=1001:
                winA=True
                break
            elif self.pointsB>=1001:
                winB=True
                break

        if winA or winB:
            for playerA in self.pairA:
                playerA.notifyGame(self.pointsA, self.pointsB)
            for playerB in self.pairB:
                playerB.notifyGame(self.pointsB, self.pointsA)

            if winA:
                print("{} have won!".format(self.pairA))
            elif winB:
                print("{} have won!".format(self.pairB))

        return self.pointsA, self.pointsB
