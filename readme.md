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
* wo wird das Netzwerk abgespeichert?
* understand policy

# DONE
* translate slowenisch/krotatisch to english
* Learning Procedure


# Learning Procedure
* train.py
  + game/play.py:  class: *game*  `play()`
    + ```SHARING PHASE```
      + game/play.py class *hand*  `play()`
        + ```Bidding PHASE```
        + ```Declaring PHASE```
        + ```Playing Phase ```: `self.currentPlayer.playCard(...)`
          + players/PlayerRL/player.py class *PlayerRL* `playCard`
          + `action_idx, log_action_prob = self.playingPolicy(state, trumpIndex, bidderIndex, legalCrds)`
          +  players/PlayerRL/policy.py class *PlayingPolicy* `forward`
        +  ```End of one Round (4 Player played their card)```
        + `notifyTrick` -> assign rewards of this round and append log_action_prob
    + Points of one Game are returned
    + `notifyHand` the policy is updated with 8 rewards and 8 log_action_prob
  + A new game is started until 1001 Points are reached!

# Playing Policy:
* It is used:  self.playingPolicy(playingState, trumpIndex, bidderIndex, legalCards)
* playingState 4x3x32 (Player x States x Cards)
  + States:
    * AVAILABLE   (cards in hand of this specific player)
    * UNAVAILABLE (already played cards of this player!)
    * TABLE       (cards on the table in general)
* TrumpIndex: Herz, Pik, Tref, Karo
* bidderIndex (active Player or bidder?!!)
* legalCards possible cards that can be played!
* Network out shape: torch.Size([1, 104]):
```
out = torch.cat((
    out418.view(out418.size(0), -1), # convert from 1,8,1,8 to 1x64 (AVAILABLE, UNAVAILABLE)
    out881.view(out881.size(0), -1), #1x32 (TABLE)
    bidder.view(bidder.size(0), -1), #1x4  (Player is bidder)
    trump.view(trump.size(0), -1)    #1x4  (Trump card)
), dim=1) # -> (batch_size, ?)
```

# Update playing Policy
* at End of one Game: in game\play.py
* ``` playerA.notifyHand(newPointsA, newPointsB)```
* goes to `self.playingPolicy.updatePolicy()`
* PlayerRL policy ->def updatePolicy(self): Line 249,
* The policy for all 8 moves is updated!
* The normalizedReward [-1, 1] for these 8 moves and the logprob is used for that!




* Index and Card:
```
  0 KARO ♦ VII
  1 KARO ♦ VIII
  2 KARO ♦ IX
  3 KARO ♦ X
  4 KARO ♦ Bube
  5 KARO ♦ DAMA
  6 KARO ♦ King
  7 KARO ♦ AS
  8 HERC ♥ VII
  9 HERC ♥ VIII
  10 HERC ♥ IX
  11 HERC ♥ X
  12 HERC ♥ Bube
  13 HERC ♥ DAMA
  14 HERC ♥ King
  15 HERC ♥ AS
  16 PIK ♠ VII
  17 PIK ♠ VIII
  18 PIK ♠ IX
  19 PIK ♠ X
  20 PIK ♠ Bube
  21 PIK ♠ DAMA
  22 PIK ♠ King
  23 PIK ♠ AS
  24 TREF ♣ VII
  25 TREF ♣ VIII
  26 TREF ♣ IX
  27 TREF ♣ X
  28 TREF ♣ Bube
  29 TREF ♣ DAMA
  30 TREF ♣ King
  31 TREF ♣ AS
```

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
