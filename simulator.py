import random
import numpy as np
import pandas as pd
import matplotlib
import argparse
import math
from player import Player, Role

class Simulator:
    def __init__(self, y1: float, y2: float, y3: float, pop_size: int, tv: float, R1: float, R2: float) -> None:
        # population proportions must cover the whole population and evenly divide (to make my life easier...)
        assert y1+y2+y3 == 1
        if (y1 * pop_size % 1 != 0 or y2 * pop_size % 1 != 0 or y3 * pop_size % 1 != 0):
            raise ValueError(f"Fractions {y1=}, {y2=}, {y3=} do not divide evenly into the population size {pop_size}")
        
        # save some important vars
        self.y1, self.y2, self.y3 = y1, y2, y3
        self.pop_size = pop_size
        self.tv = tv
        self.R1, self.R2 = R1, R2

        # compute population proportions
        self.x1, self.x2, self.x3 = self.y1 * self.pop_size, self.y2 * self.pop_size, self.y3 * self.pop_size

        # add players to game
        self.players = []
        for _ in range(self.x1):
            self.players.append(Player(Role.CITIZEN))
        for _ in range(self.x2):
            self.players.append(Player(Role.GOOD_GOVERNOR))
        for _ in range(self.x3):
            self.players.append(Player(Role.BAD_GOVERNOR))

    def step(self) -> None:
        for player in self.players:
            player.play(self.x1, self.x2, self.x3, self.tv, self.R1, self.R2)

    def reproduce(self) -> None:
        children = []
        fitnesses = [player.fitness for player in self.players]
        probs = [fitness / sum(fitnesses) for fitness in fitnesses]
        randoms = [random.random() for _ in range(len(fitnesses))]

        # reproduction is weighted by fitness
        choices = [prob <= random for prob, random in zip(probs, randoms)]
        for (player, choice) in zip(self.players, choices):
            children.append(player.reproduce(choice))
        self.update_population(children)

    def update_population(self, children) -> None:
        citizens, good, bad = 0, 0, 0
        for child in children:
            if child.role == Role.CITIZEN:
                citizens += 1
            elif child.role == Role.GOOD_GOVERNOR:
                good += 1
            else:
                bad += 1
        self.x1, self.x2, self.x3 = citizens, good, bad
        self.y1, self.y2, self.y3 = self.x1 / self.pop_size, self.x2 / self.pop_size, self.x3 / self.pop_size

    def run(self, iters: int) -> None:
        for _ in range(iters):
            self.step()
        self.reproduce()

# Set up cmd line args
parser = argparse.ArgumentParser(prog='N-player trust game simulator', description='Simulates the N-player trust game')
parser.add_argument('y1', type=float)
parser.add_argument('y2', type=float)
parser.add_argument('y3', type=float)
parser.add_argument('pop_size', type=int)
parser.add_argument('tv', type=float)
parser.add_argument('iters', type=int)
parser.add_argument('R1', type=float)
parser.add_argument('R2', type=float)

def main():
    args = parser.parse_args()
    simulator = Simulator(args.y1, args.y2, args.y3, args.pop_size, args.tv, args.R1, args.R2)
    
    simulator.run(args.iters)