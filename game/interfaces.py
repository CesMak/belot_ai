from abc import ABCMeta, abstractmethod
import game.belot as belot

class IPlayer(metaclass=ABCMeta):
    '''
    Apstraktni razred koji predstavlja sučelje jednog igrača (agenta) prema igri
    An abstract class that represents a single player (agent) interface to the game
    '''

    def __init__(self, name, human=False):
        self.name=name
        self.human=human
        self.initialize()

    def __eq__(self, other):
        if other==None:
            return False

        return self.name==other.name

    def __hash__(self):
        return self.name.__hash__()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def updateCards(self, cards):
        '''
        Metoda koja uručuje karte igraču.
        The method of handing cards to a player.
        '''

        # self.cards = sorted(cards)
        self.cards = cards
        self.notifyCards()

    def declare(self):
        '''
        Metoda koja vraća dvije liste:
        listu (list) skupova (set) karata koji čine zvanja te
        listu (list) vrijednosti (int) svakog pojedinog zvanja.
        A method that returns two lists:
        list of sets of cards that make up the vocations and
        a list (list) of the values ​​(int) of each individual vocation.
        '''

        declarationCards=belot.declarationCards
        declarationValues=belot.declarationValues

        foundCards=[]
        foundValues=[]

        for i in range(len(declarationCards)):
            setOfCards=declarationCards[i]
            setValue=declarationValues[i]
            if setOfCards.issubset(self.cards):
                foundCards.append(setOfCards)
                foundValues.append(setValue)

        uniqueDeclarations=[]
        uniqueValues=[]
        for i in range(len(foundCards)):
            subset=False
            for j in range(len(foundCards)):
                if i!=j:
                    if foundCards[i].issubset(foundCards[j]):
                        subset=True
                        break
            if not subset:
                uniqueDeclarations.append(foundCards[i])
                uniqueValues.append(foundValues[i])

        return uniqueDeclarations, uniqueValues

    @abstractmethod
    def initialize(self):
        '''
        Metoda koja služi za inicijalizaciju svih potrebnih atributa.
        A method used to initialize all the required attributes.
        '''
        pass

    @abstractmethod
    def notifyCards(self):
        '''
        Metoda koja dojavljuje da su karte podijeljene i da se nalaze
        u self.cards.
        A method that reports that maps are divided and are located in self.cards.
        '''
        pass

    @abstractmethod
    def notifyTrumpSuit(self, trumpSuit, bidder):
        '''
        A method that reports which color is called trump (TrumpSuit) and which player called it (bidder).
        trumpSuit is one of the values ​​from belot.suits.
        bidder is one of the values ​​of belot.PlayerRole:
        - belot.PlayerRole.ME -> me
        - belot.PlayerRole.LEFT_OPPONENT -> opponent on the left
        - belot.PlayerRole.RIGHT_OPPONENT -> opponent on the right
        - belot.PlayerRole.TEAMMATE -> teammate
        '''
        pass

    @abstractmethod
    def notifyDeclarations(self, declarations):
        '''
        The method reports the vocations of all players.
        'declarations' is a dict to which the key is the player,
        and the value of the list of sets of cards that make up the vocation.
        Keys:
        - belot.PlayerRole.ME -> me
        - belot.PlayerRole.LEFT_OPPONENT -> opponent on the left
        - belot.PlayerRole.RIGHT_OPPONENT -> opponent on the right
        - belot.PlayerRole.TEAMMATE -> teammate
        '''
        pass

    @abstractmethod
    def notifyTrick(self, cards, value):
        '''
        The method reports the end of the trick.
        'cards' are cards contained in a trick, and 'value' is the value of a trick.
        If value> 0 the trash is obtained, and if the value <0 the trash is lost.
        '''
        pass

    @abstractmethod
    def notifyHand(self, pointsUs, pointsThem):
        '''
        Method announces end of sharing.
        'pointsUs' are earned points of your own team and 'pointsThem' are earned points of the opposing team.
        '''
        pass

    @abstractmethod
    def notifyGame(self, pointsUs, pointsThem):
        '''
        The method reports the end of the game.
        at the end of the game update only the biddingPolicy
        'pointsUs' are earned points of your own team and 'pointsThem' are earned points of the opposing team.
        '''
        pass

    @abstractmethod
    def notifyBela(self, player, card):
        '''
        The method reports when a player calls white.
        'player' is a player called white and 'card' is a card that is thrown.
        '''
        pass

    @abstractmethod
    def bid(self, must):
        '''
        Method for calling trump. Must return one of the values ​​from belot.suits or
        None if the player does not want to call.
        If 'must' is set to True, the player must call (on mus).
        '''
        return None

    @abstractmethod
    def playCard(self, table, legalCards):
        '''
        A method for playing the map. Must return one of the values ​​from legalCards.
        legalCards is a subset of cards in the hand that a player can play at any given time.
        'tables' is a dictionary (dict) that represents the state of the cards on the table. The key is
        player, and value is the card that player threw.
        Keys:
        - belot.PlayerRole.LEFT_OPPONENT -> opponent on the left
        - belot.PlayerRole.RIGHT_OPPONENT -> opponent on the right
        - belot.PlayerRole.TEAMMATE -> teammate
        '''
        return None

    @abstractmethod
    def declareBela(self, table):
        '''
        A method that determines whether a player calls white or not. Must return True or False.
        'tables' is a dictionary (dict) that represents the state of the cards on the table. The key is
        player, and value is the card that player threw.
        Keys:
        - belot.PlayerRole.LEFT_OPPONENT -> opponent on the left
        - belot.PlayerRole.RIGHT_OPPONENT -> opponent on the right
        - belot.PlayerRole.TEAMMATE -> teammate
        '''
        return False
