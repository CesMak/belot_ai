from typing import List

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.distributions import Categorical
import numpy as np

import game.belot as belot
from game.belot import cards
from .loss import PolicyGradientLoss

_device = torch.device("cpu")
if torch.cuda.is_available():
    _device = torch.device("cuda")
    print("I USE CUDA NOW!!!")
else:
    print("I CANNOT USE CUDA -> USE CPU")

class BiddingPolicy(nn.Module):
    '''
    Trumpf Wahl:
    Eingänge: 4 (Suits)
    Ausgang:  4 (Suits)

    TODO warum 61x5 (als ausgang?)
    '''
    def __init__(self):
        super().__init__()

        # Network
        in_channels = 4 # KARO, HERC, PIK, TREF
        out_channels = in_channels

        self.conv222 = nn.Conv1d(in_channels, out_channels, kernel_size=2, stride=2, dilation=2)
        self.conv211 = nn.Conv1d(in_channels, out_channels, kernel_size=2, stride=1, dilation=1)
        self.conv213 = nn.Conv1d(in_channels, out_channels, kernel_size=2, stride=1, dilation=3)
        self.classify = nn.Linear(61, 4 + 1) #  KARO, HERC, PIK, TREF, dalje
        # dalje =  gibt die Trumpfwahl weiter

        # Optimizer
        self.optimizer = optim.SGD(self.parameters(), lr=1e-2, momentum=0.9)

        # Criterion
        self.criterion = PolicyGradientLoss()

        # Keep track of actions and rewards during a single game (i.e. multiple hands)
        # This will be used to build a batch (torch.cat) passed to the criterion
        self.log_action_probabilities = list()
        self.rewards = list()
        self.musts = list()

        self.to(_device)

    def forward(self, state: np.ndarray, must):
        state = torch.Tensor(state)

        # Add batch dimension if not present
        if state.dim() == 2:
            state = state.unsqueeze(dim=0)

        state = state.to(_device)

        if isinstance(must, bool):
            must = [must]
            # Remember if it was a must
            self.musts += must
        elif not isinstance(must, list):
            raise ValueError(f"'must' should be either a bool or a list! ({type(must)})")

        must = torch.Tensor(must).unsqueeze(dim=1).to(_device)

        # state -> (batch_size, in_channels, num_cards)
        # must -> (batch_size, 1)

        out222 = F.relu(self.conv222(state)) # -> (batch_size, out_channels, 3)
        out211 = F.relu(self.conv211(state)) # -> (batch_size, out_channels, 7)
        out213 = F.relu(self.conv213(state)) # -> (batch_size, out_channels, 5)

        out = torch.cat((out222, out211, out213), dim=2) # -> (batch_size, out_channels, 15)
        out = out.view(out.size(0), -1) # flatten -> (batch_size, 4 * 15 = 60)
        out = torch.cat((out, must), dim=1) # concatenate with must info -> (batch_size, 60 + 1 = 61)

        probs = F.softmax(self.classify(out), dim=1)
        if must[0]:
            mask = torch.ones(4 + 1).to(_device)
            mask[4] = 0
            probs = probs * mask

        # Get action
        distribution = Categorical(probs)
        action_idx = distribution.sample()
        log_action_probability = distribution.log_prob(action_idx)

        # Remember the log-probability
        self.log_action_probabilities.append(log_action_probability)

        return action_idx.item(), log_action_probability

    def feedback(self, reward: float):
        self.rewards.append(reward)

    def updatePolicy(self):
        # Log-probabilites of performed actions
        log_action_probabilities = torch.cat(self.log_action_probabilities, dim=0)

        # Rewards (do not reward if bidding was a must)
        rewards = list(map(
            lambda pair: 0 if pair[1] else pair[0],
            zip(self.rewards, self.musts)
        ))

        rewards = torch.tensor(rewards).unsqueeze(dim=1).to(_device)

        # Optimization step
        self.optimizer.zero_grad()
        loss = self.criterion(log_action_probabilities, rewards)
        loss.backward()
        self.optimizer.step()

        # Reset the log-probabilites and rewards
        self.log_action_probabilities.clear()
        self.rewards.clear()
        self.musts.clear()


class PlayingPolicy(nn.Module):

    def __init__(self):
        super().__init__()

        # Parameters
        self.gamma = 0.9 # reward discount factor

        # Network
        in_channels = 4 # four players
        out_channels = 8

        self.conv418 = nn.Conv2d(in_channels, out_channels, kernel_size=(3, 4), stride=1, dilation=(1, 8))
        self.conv881 = nn.Conv2d(in_channels, out_channels, kernel_size=(3, 8), stride=8, dilation=(1, 1))
        self.classify = nn.Linear(104, len(belot.cards)) #  KARO, HERC, PIK, TREF, dalje

        # Optimizer
        self.optimizer = optim.SGD(self.parameters(), lr=1e-2, momentum=0.9)

        # Criterion
        self.criterion = PolicyGradientLoss()

        # Keep track of actions and rewards during a single game (i.e. multiple hands)
        # This will be used to build a batch (torch.cat) passed to the criterion
        self.log_action_probabilities = list()
        self.rewards = list()

        self.to(_device)

    def forward(self, state: np.ndarray, bidder, trump, legalCards):
        # State
        state = torch.Tensor(state)
        if state.dim() == 3:
            state = state.unsqueeze(dim=0)

        state = state.to(_device)

        # Bidder
        if isinstance(bidder, int):
            bidder = [bidder]
        elif not isinstance(bidder, list):
            raise ValueError(f"'bidder' should be either an int or a list! ({type(must)})")

        bidder_tensors = list()
        for bidderIndex in bidder:
            t = torch.zeros(len(belot.PlayerRole))
            t[bidderIndex] = 1
            bidder_tensors.append(t)

        bidder = torch.stack(bidder_tensors, dim=0).to(_device)

        # Trump
        if isinstance(trump, int):
            trump = [trump]
        elif not isinstance(bidder, list):
            raise ValueError(f"'trump' should be either an int or a list! ({type(must)})")

        trump_tensors = list()
        for trumpIndex in trump:
            t = torch.zeros(len(belot.Suit))
            t[trumpIndex] = 1
            trump_tensors.append(t)

        trump = torch.stack(trump_tensors, dim=0).to(_device)

        # Legal mask
        mask = torch.zeros(1, len(belot.cards))
        for legalCard in legalCards:
            idx = belot.cards.index(legalCard)
            mask[:, idx] = 1
        mask = mask.to(_device)

        # state -> 4 (players), 3 (card states), 32 (cards)
        out418 = F.relu(self.conv418(state)) # -> (batch_size, out_channels, ?, ?)
        out881 = F.relu(self.conv881(state)) # -> (batch_size, out_channels, ?, ?)

        out = torch.cat((
            out418.view(out418.size(0), -1),
            out881.view(out881.size(0), -1),
            bidder.view(bidder.size(0), -1),
            trump.view(trump.size(0), -1)
        ), dim=1) # -> (batch_size, ?)


        probs = F.softmax(self.classify(out), dim=1)
        probs = probs * mask

        # Get action
        distribution = Categorical(probs)
        action_idx = distribution.sample()
        log_action_probability = distribution.log_prob(action_idx)

        # Remember the log-probability
        self.log_action_probabilities.append(log_action_probability)

        return action_idx.item(), log_action_probability

    def feedback(self, reward: float):
        self.rewards.append(reward)

    def updatePolicy(self):
        # Log-probabilites of performed actions
        log_action_probabilities = torch.cat(self.log_action_probabilities, dim=0)

        # Rewards (do not reward if bidding was a must)
        discountedRewards = list()
        numRewards = len(self.rewards)
        for i in range(numRewards):
            realReward = 0

            for j in range(i, numRewards):
                reward = self.rewards[j]
                realReward += reward * np.power(self.gamma, j - i)

            discountedRewards.append(realReward)

        rewards = torch.tensor(discountedRewards).unsqueeze(dim=1).to(_device)

        # Optimization step
        self.optimizer.zero_grad()
        loss = self.criterion(log_action_probabilities, rewards)
        loss.backward()
        self.optimizer.step()

        # Reset the log-probabilites and rewards
        self.log_action_probabilities.clear()
        self.rewards.clear()
