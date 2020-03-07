Testing:

```
python train.py
```

Some docu in interfaces.py

# Rules (Belote 4 Players)
  * [de_wiki](https://de.wikipedia.org/wiki/Belote) and [wiki_Belot](https://de.wikipedia.org/wiki/Belot)
* 32 Cards (4 per Person)
* Bidding process (Choosing trump card)
  + First 6 cards are handed to each player
  + First Player can choose trump card or says further
  + If none of the other players chooses a trump, first player has to choose the trump!
  + The team which chooses the trump is the bidding Team
* Declaring process
  + 3 Karten derselben Farbe hintereinander ergeben 20 Punkte (Bsp: 7-8-9 oder 10-Bube-Dame)
  + 4 Karten derselben Farbe hintereinander ergeben 50 Punkte (Bsp: 9-10-Bube-Dame oder 7-8-9-10)
  + 4 Karten der gleichen Symbole ergeben 100 Punkte (Bsp: 4× 10 oder 4× Dame oder 4× König oder 4× Ass)
  + 4 Karten mit der "9" ergeben 150 Punkte
  + 4 Karten mit dem Symbol der Buben ergeben 200 Punkte
  + 5 Karten derselben Farbe hintereinander ergeben 100 Punkte (Bsp: 10-Bube-Dame-König-As oder 8-9-10-Bube-Dame)
* Playing process
  + Es wird immer über Kreuz gespielt (dein Teammate sitzt dir gegenüber)
  + Reihenfolge: 7,8,9,Bube,Dame,König, 10, As
  + Es gilt also Trumpfzwang in allen Farben und Stichzwang in der Trumpffarbe.
* End of Game:
  + You need more points than (162+declaredValues)/2+1 otherwise you get 0 points and enemy gets your points
  + Points:
    + Suit.Trump: 7, 8: 0   9: 14 10:10, Bube: 20, Dame 3, King 4, As: 11
    + Suit. Non Trump: 7,8,9: 0, 10:10, Bube:2, Dame: 3, King:4, As:11
  + The one who reaches 1001 points

# TODO
* translate slowenisch/krotatisch to english
* wo wird das Netzwerk abgespeichert?


# Result
```
Sharing Points:
	Me (Keyboard) i Friend (Random): 74
	Markus (RL) i Laura (RL): 128
Total points:
	Me (Keyboard) i Friend (Random): 324
	Markus (RL) i Laura (RL): 262
```

# Training:
```
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 40.0% (40 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 34.0% (34 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 36.0% (36 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 41.0% (41 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 31.0% (31 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 44.0% (44 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 42.0% (42 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 44.0% (44 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 49.0% (49 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 49.0% (49 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 41.0% (41 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 49.0% (49 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 43.0% (43 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 42.0% (42 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 43.0% (43 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 46.0% (46 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 48.0% (48 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 38.0% (38 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 45.0% (45 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 46.0% (46 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 43.0% (43 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 35.0% (35 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 35.0% (35 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 51.0% (51 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 47.0% (47 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 43.0% (43 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 46.0% (46 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 51.0% (51 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 46.0% (46 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 39.0% (39 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 43.0% (43 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 42.0% (42 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 43.0% (43 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 49.0% (49 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 45.0% (45 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 42.0% (42 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 50.0% (50 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 44.0% (44 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 47.0% (47 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 46.0% (46 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 46.0% (46 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 51.0% (51 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 41.0% (41 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 45.0% (45 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 38.0% (38 / 100)
Traceback (most recent call last):
  File "train.py", line 35, in <module>
    pointsA, pointsB = game.play()
  File "/home/markus/Documents/06_Software_Projects/belot/game/play.py", line 392, in play
    newPointsA, newPointsB = hand.play()
  File "/home/markus/Documents/06_Software_Projects/belot/game/play.py", line 262, in play
    card = self.currentPlayer.playCard(localTable, playerLegalCards)
  File "/home/markus/Documents/06_Software_Projects/belot/players/PlayerRL/player.py", line 95, in playCard
    action_idx, log_action_probability = self.playingPolicy(playingState, trumpIndex, bidderIndex, legalCards)
  File "/home/markus/Documents/06_Software_Projects/belot/belot_env/lib/python3.6/site-packages/torch/nn/modules/module.py", line 532, in __call__
    result = self.forward(*input, **kwargs)
  File "/home/markus/Documents/06_Software_Projects/belot/players/PlayerRL/policy.py", line 208, in forward
    action_idx = distribution.sample()
  File "/home/markus/Documents/06_Software_Projects/belot/belot_env/lib/python3.6/site-packages/torch/distributions/categorical.py", line 107, in sample
    sample_2d = torch.multinomial(probs_2d, 1, True)
RuntimeError: invalid multinomial distribution (encountering probability entry < 0)
```

* winningPercentage = 50%
```
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 31.0% (31 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 48.0% (48 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 31.0% (31 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 39.0% (39 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 45.0% (45 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 46.0% (46 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 47.0% (47 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 44.0% (44 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 48.0% (48 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 44.0% (44 / 100)
[RL] Markus (RL) i Laura (RL) - postotak pobjeda (u zadnjih 100 igara): 44.0% (44 / 100)
0:27:35.980478
PAIR A: Me (Keyboard) i Friend (Random)
PAIR B:: Markus (RL) i Laura (RL)
================= SHARING =================
Card dealer Me (Keyboard)
---------- Markus (RL) ----------
Markus (RL) calling 0
Vocations:
	Me (Keyboard): [{HERC ♥ DEČKO, HERC ♥ IX, HERC ♥ X}]

---------- Markus (RL) ----------
TREF ♣ KRALJ
---------- Friend (Random) ----------
TREF ♣ IX
---------- Laura (RL) ----------
TREF ♣ X
---------- Me (Keyboard) ----------
Cards:  [KARO ♦ X, HERC ♥ X, PIK ♠ IX, HERC ♥ IX, HERC ♥ DEČKO, HERC ♥ AS, PIK ♠ X, KARO ♦ IX]
[1] KARO ♦ X
[2] KARO ♦ IX
Ticket number::
```
