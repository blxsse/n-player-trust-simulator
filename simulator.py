import argparse
import random

import matplotlib.pyplot as plt
from tqdm import tqdm

from player import Player, Role

class Simulator:
    """Simulates an N-Player Trust Game with iters rounds and a population size of pop_size, evenly divided such that
    y1 is the fraction of players who are citizens, y2 the fraction of trustworthy governors, and y3 the fraction of
    untrustworthy governors. tv is the value citizens initially pay, while R1 and R2 are the constants used by the
    trustworthy and untrustworthy governors, respectively."""

    def __init__(self, y1: float, y2: float, y3: float, pop_size: int, tv: float, R1: float, R2: float, iters: int) -> None:
        # population proportions must cover the whole population and evenly divide (to make my life easier...)
        assert y1+y2+y3 == 1
        if (y1 * pop_size % 1 != 0 or y2 * pop_size % 1 != 0 or y3 * pop_size % 1 != 0):
            raise ValueError(f"Fractions {y1=}, {y2=}, {y3=} do not divide evenly into the population size {pop_size}")
        
        # save some important vars
        self.y1, self.y2, self.y3 = y1, y2, y3
        self.pop_size = pop_size
        self.tv = tv
        self.R1, self.R2 = R1, R2
        self.iters = iters

        # compute population proportions
        self.x1, self.x2, self.x3 = int(self.y1 * self.pop_size), int(self.y2 * self.pop_size), int(self.y3 * self.pop_size)

        # add players to game
        self.players = []
        for _ in range(self.x1):
            self.players.append(Player(Role.CITIZEN))
        for _ in range(self.x2):
            self.players.append(Player(Role.GOOD_GOVERNOR))
        for _ in range(self.x3):
            self.players.append(Player(Role.BAD_GOVERNOR))

        # add history, for plotting
        self.history = {'y1': [], 'y2': [], 'y3': []}

    def step(self) -> None:
        """Updates each player's fitness based on their move according to their role."""
        for player in self.players:
            player.play(self.x1, self.x2, self.x3, self.tv, self.R1, self.R2)

    def reproduce(self) -> None:
        """Generates the next generation of players based on fitness of current players."""
        children = []
        fitnesses = [player.fitness for player in self.players]
        probs = [(fitness / sum(fitnesses)) for fitness in fitnesses]
        randoms = [random.random() for _ in range(len(fitnesses))]

        # reproduction is weighted by fitness
        choices = [rand <= prob for prob, rand in zip(probs, randoms)]
        for (player, choice) in zip(self.players, choices):
            children.append(player.reproduce(choice))
        self.update_population(children)

    def update_population(self, children) -> None:
        """Updates population proportions after reproduction."""
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

    def run(self) -> None:
        """Runs the simulation and reproduction for given amount of iterations."""
        for _ in tqdm(range(self.iters)):
            self.history['y1'].append(self.y1)
            self.history['y2'].append(self.y2)
            self.history['y3'].append(self.y3)
            self.step()
            self.reproduce()

    def plot(self) -> None:
        """Displays population proportions as a function of time."""
        # set up plot
        plt.plot(range(self.iters), self.history['y1'], label='Citizens')
        plt.plot(range(self.iters), self.history['y2'], label='Trustworthy governors')
        plt.plot(range(self.iters), self.history['y3'], label='Untrustworthy governors')

        # add labels and title
        plt.xlabel('Iter')
        plt.ylabel('Proportion')
        plt.title('N-player trust game simulation')
        plt.legend()

        plt.show()

# Set up cmd line args
parser = argparse.ArgumentParser(prog='N-player trust game simulator', description='Simulates the N-player trust game')
parser.add_argument('--y1', type=float, help='Proportion of citizens')
parser.add_argument('--y2', type=float, help='Proportion of trustworthy governors')
parser.add_argument('--y3', type=float, help='Proportion of untrustworthy governors')
parser.add_argument('--pop_size', type=int, help='Population size')
parser.add_argument('--tv', type=float, help='Trusted value; how much a citizen pays')
parser.add_argument('--iters', type=int, help='Number of rounds in simulation')
parser.add_argument('--R1', type=float, help='Constant for trustworthy governors')
parser.add_argument('--R2', type=float, help='Constant for untrustworthy governors')

def main():
    args = parser.parse_args()
    simulator = Simulator(args.y1, args.y2, args.y3, args.pop_size, args.tv, args.R1, args.R2, args.iters)
    
    simulator.run()
    simulator.plot()

if __name__ == '__main__':
    main()
