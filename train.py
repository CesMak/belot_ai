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
playerA1 = PlayerRL("Markus_(RL)")
playerA2 = PlayerRL("Laura_(RL)")
pairA = Pair(playerA1, playerA2)

# Ein paar spielt zufaellig: Par koji igra nasumično
playerB1 = PlayerRandom("Matti_(Random)")
playerB2 = PlayerRandom("Rahel_(Random)")
pairB = Pair(playerB1, playerB2)

def train_player():
    # Treniraj # Zug
    stdout.disable()

    games = 10000 #10000, one game means up to 1001 Points!!!
    last  = 1000
    wins  = list()

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
            if winningPercentage >= 90:#90 before
                break
            game.saveNetworks(str(i))
            stdout.enable()
            print("[RL] {} - win percentage (in last 100 games): {}% ({} / {}) at game:".format(pairA, last, winningPercentage, winsA, last), i, (datetime.datetime.now() - now))
            stdout.disable()

    # Igraj # spielen
    #stdout.enable()
    game.saveNetworks()
    print(datetime.datetime.now() - now)

    playerA1.eval()
    playerA2.eval()

def play_():
    pairB = Pair(PlayerKeyboard("Me_(Keyboard)"), PlayerRandom("Friend_(Random)"))
    game = Game(pairA, pairB)

    pointsA, pointsB = game.play()

play_()
#train_player()
