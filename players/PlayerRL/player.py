import game.belot as belot
from game.interfaces import IPlayer

from enum import Enum
from .policy import BiddingPolicy
from .policy import PlayingPolicy

import numpy as np
from math import pow

"""
    Ulaz u neuronsku mrežu:
        LEFT_OPPONNENT: 32 x (AVAILABLE, TABLE, UNAVAILABLE): 96
        RIGHT_OPPONNENT: 32 x (AVAILABLE, TABLE, UNAVAILABLE): 96
        TEAMMATE: 32 x (AVAILABLE, TABLE, UNAVAILABLE): 96
        ME: 32 x (AVAILABLE, UNAVAILABLE): 64
        TRUMP: 4
        BIDDER: 4
    = 360
"""

class CardState(Enum):
    UNKNOWN = 0     # Es ist nicht bekannt, wo sich die Karte befindet
    AVAILABLE = 1   # jemand hat eine Karte in der Hand (je nach Ansagen ist das bekannt!)
    TABLE = 2       # Karte liegt auf dem Tisch
    UNAVAILABLE = 3 # Karte wurde bereits gespielt

class PlayerRL(IPlayer):

    def initialize(self):
        self.train()

        # Status und entsprechende Belohnungen haben die Karte bereits gespielt
        # für das neuronale Netzwerk, das die nächste Karte bestimmt
        self.playingDiscount = 0.95
        self.playingReward = 0
        self.trickNumber = 0

        self.playingPolicy = PlayingPolicy()

        # für das neuronale Netzwerk, das den Trumpf bestimmt
        self.biddingPolicy = BiddingPolicy()

        # Karten gespielt
        self.playedCards = set()

        # own knowledge of the game
        self.knowledge = dict()

        # initially put all the cards in the UNKNOWN state
        self.knowledge[CardState.UNKNOWN] = set(belot.cards)

        # initialize sets for each player
        for player in [belot.PlayerRole.LEFT_OPPONENT, belot.PlayerRole.TEAMMATE, belot.PlayerRole.RIGHT_OPPONENT]:
            self.knowledge[player] = dict()
            for cardStatus in [CardState.AVAILABLE, CardState.UNAVAILABLE, CardState.TABLE]:
                self.knowledge[player][cardStatus] = set()

    def notifyCards(self):
        # remove the UNKNOWN ticket in your hand
        self.knowledge[CardState.UNKNOWN] -= set(self.cards)

    def notifyTrumpSuit(self, trumpSuit, bidder):
        self.trumpSuit = trumpSuit
        self.bidder = bidder

    def notifyDeclarations(self, declarations):
        knowledge = self.knowledge

        # transfer all known maps from the vocation to AVAILABLE
        for player in declarations:
            if player != belot.PlayerRole.ME:
                for declaredSet in declarations[player]:
                    knowledge[CardState.UNKNOWN] -= declaredSet
                    knowledge[player][CardState.AVAILABLE] |= declaredSet

    def playCard(self, table, legalCards):
        knowledge = self.knowledge

        # put the charts on the table in the TABLE state
        for player in table:
            card = table[player]

            if card in knowledge[player][CardState.AVAILABLE]:
                knowledge[player][CardState.AVAILABLE].remove(card)
            elif card in knowledge[CardState.UNKNOWN]:
                knowledge[CardState.UNKNOWN].remove(card)

            knowledge[player][CardState.TABLE].clear()
            knowledge[player][CardState.TABLE].add(card)

        # playing policy network
        playingState, trumpIndex, bidderIndex = self.playingState
        print("RL-player.py playCard")
        print("trumpIndex", trumpIndex, "bidderIndex", bidderIndex)
        print("leagalCards", legalCards)
        action_idx, log_action_probability = self.playingPolicy(playingState, trumpIndex, bidderIndex, legalCards)


        cardToPlay = belot.cards[action_idx]
        print("action_idx", action_idx, "which is", cardToPlay, "log_action_probability", log_action_probability)

        #transfer all TABLE maps to UNAVAILABLE
        for player in table:
            knowledgeTableCopy = set(knowledge[player][CardState.TABLE])
            for card in knowledgeTableCopy:
                knowledge[player][CardState.TABLE].remove(card)
                knowledge[player][CardState.UNAVAILABLE].add(card)

        self.playedCards.add(cardToPlay)
        return cardToPlay

    def bid(self, must):
        # bidding policy network
        biddingState = self.biddingState

        options = list(belot.Suit) + [None]
        action_idx, log_action_probability = self.biddingPolicy(biddingState, must)

        return options[action_idx]

    def notifyHand(self, pointsUs, pointsThem):
        # if len(self.biddingActions) == len(self.biddingRewards) + 1:
        #     normalizedReward = pointsUs / 81 - 1
        #     self.biddingRewards.append(normalizedReward)

        self.playingPolicy.updatePolicy()

        # reset
        self.playedCards.clear()

        # initially put all the cards in the UNKNOWN state
        self.knowledge.clear()
        self.knowledge[CardState.UNKNOWN] = set(belot.cards)

        for player in [belot.PlayerRole.LEFT_OPPONENT, belot.PlayerRole.TEAMMATE, belot.PlayerRole.RIGHT_OPPONENT]:
            self.knowledge[player] = dict()
            for cardStatus in [CardState.AVAILABLE, CardState.UNAVAILABLE, CardState.TABLE]:
                self.knowledge[player][cardStatus] = set()

    def notifyTrick(self, cards, value):
        normalizedReward = value / 56
        self.playingPolicy.feedback(normalizedReward)

    def notifyGame(self, pointsUs, pointsThem):
        # train trunk for calling trump
        self.biddingPolicy.updatePolicy()

    def notifyBela(self, player, card):
        pass

    def declareBela(self, table):
        # TODO bela declaring policy network
        choice = True

        return choice

    def train(self):
        self.train = True

    def eval(self):
        self.train = False

    @property
    def playingState(self) -> np.ndarray:
        knowledge = self.knowledge
        cardStates = [
            CardState.AVAILABLE,
            CardState.UNAVAILABLE,
            CardState.TABLE
        ]

        state = np.zeros(
            shape=(len(belot.PlayerRole), len(cardStates), len(belot.cards))
        )
        #print(state.shape) # 4, 3, 32

        otherPlayers = [
            belot.PlayerRole.TEAMMATE,
            belot.PlayerRole.LEFT_OPPONENT,
            belot.PlayerRole.RIGHT_OPPONENT,
        ]
        for i, player in enumerate(otherPlayers):
            for j, cardState in enumerate(cardStates):
                # For the cards you know where they are, schedule them with security
                for card in knowledge[player][cardState]:
                    k = belot.cards.index(card)
                    state[i, j, k] = 1

                # If you do not know where the ticket is, arrange it uniformly
                # Player Probabilities as AVAILABLE (0)
                for unknownCard in knowledge[CardState.UNKNOWN]:
                    k = belot.cards.index(unknownCard)
                    state[i, 0, k] = 1 / len(otherPlayers)

        # Ja
        cardStates = [CardState.AVAILABLE, CardState.UNAVAILABLE]

        for cards, cardState in [(self.cards, CardState.AVAILABLE), (self.playedCards, CardState.UNAVAILABLE)]:
            for card in cards:
                j = cardStates.index(cardState)
                k = belot.cards.index(card)
                state[-1, j, k] = 1

        # What color is the trump card
        trumpIndex = self.trumpSuit

        # Which player he called
        bidderIndex = list(belot.PlayerRole).index(self.bidder)

        return state, trumpIndex, bidderIndex

    @property
    def biddingState(self) -> np.ndarray:
        suits = list(belot.Suit)
        ranks = list(belot.Rank)

        state = np.zeros(
            shape=(len(suits), len(ranks)),
            dtype=np.float32
        )

        for card in self.cards:
            i = suits.index(card.suit)
            j = ranks.index(card.rank)
            state[i][j]=1

        return state
