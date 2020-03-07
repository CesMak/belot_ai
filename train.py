#!/usr/bin/python3

from game.play import Pair, Game
from players.PlayerRandom import PlayerRandom
from players.PlayerKeyboard import PlayerKeyboard
from players.PlayerRL import PlayerRL
import datetime
import stdout

# RL par
# TODO save & load policy networks
# TODO share policy networks across all RL players
playerA1 = PlayerRL("Markus (RL)")
playerA2 = PlayerRL("Laura (RL)")
pairA = Pair(playerA1, playerA2)

# Ein paar spielt zufällig: Par koji igra nasumično
playerB1 = PlayerRandom("Matti (Random)")
playerB2 = PlayerRandom("Rahel (Random)")
pairB = Pair(playerB1, playerB2)

def train_player():
    # Treniraj # Zug
    #stdout.disable()

    games = 10000
    last = 100
    wins = list()

    #Training:
    print("inside train player")
    now = datetime.datetime.now()
    for i in range(games):
        game = Game(pairA, pairB)
        pointsA, pointsB = game.play()
        wins.append("A" if pointsA > pointsB else "B")

        if i > 0 and i % last == 0:
            winsA = wins[-last:].count("A")
            winningPercentage = winsA / last * 100
            if winningPercentage >= 51:#90 before
                break
            #stdout.enable()
            #
            print("[RL] {} - win percentage (in last 100 games): {}% ({} / {})".format(pairA, last, winningPercentage, winsA, last))
            #stdout.disable()

    # Igraj # spielen
    #stdout.enable()
    print(datetime.datetime.now() - now)

    playerA1.eval()
    playerA2.eval()

def play_():
    pairB = Pair(PlayerKeyboard("Me (Keyboard)"), PlayerRandom("Friend (Random)"))
    game = Game(pairA, pairB)

    pointsA, pointsB = game.play()

#play_()
train_player()
