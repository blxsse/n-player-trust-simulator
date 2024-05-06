import argparse
import math

import matplotlib.pyplot as plt
from tqdm import tqdm

def simplex_map(point):
    """Generates coordinate of point in equilateral 1-length triangle simplex based on weights in point."""
    weighted_one = point[0] * 1, 0
    weighted_three = point[2] * 0.5, point[2] * math.sqrt(3) / 2

    return (weighted_one[0] + weighted_three[0]) , (weighted_one[1] + weighted_three[1]) 

class Simulator:
    """Simulates an N-Player Trust Game with iters rounds and a population size of pop_size, evenly divided such that
    y1 is the fraction of players who are citizens, y2 the fraction of trustworthy governors, and y3 the fraction of
    untrustworthy governors. tv is the value citizens initially pay, while R1 and R2 are the constants used by the
    trustworthy and untrustworthy governors, respectively."""

    def __init__(self, y1: float, y2: float, y3: float, tv: float, R1: float, R2: float, iters: int, dt: float = 0.01) -> None:
        # population proportions must cover the whole population
        assert abs(y1+y2+y3-1) < 0.0000000001
        
        # save some important vars
        self.y1, self.y2, self.y3 = y1, y2, y3
        self.tv = tv
        self.R1, self.R2 = R1, R2
        self.iters = iters
        self.dt = dt

        # add history, for plotting
        self.history = {'y1': [], 'y2': [], 'y3': []}

    def step(self) -> None:
        """Simulates one step of the replicator equations."""
        one = (self.y1 * self.y1 * self.tv) / (1 - self.y1)
        two = self.y2 * (1 - 2 * self.R1) + self.y3 * (1 - self.R2)
        three = (self.y1 * self.tv) / (1 - self.y1)
        four = self.y2 * (self.R1 - 1) - self.y3
        d_y1 = one * two + three * four 
        d_y2 = (self.y1 * self.y2 * self.tv)/(1 - self.y1) * (self.y2 * (1 - 2 * self.R1) + self.y3 * (1 - self.R2) + self.R1)
        d_y3 = (self.y1 * self.y3 * self.tv)/(1 - self.y1) * (self.y2 * (1 - 2 * self.R1) + self.y3 * (1 - self.R2) + self.R2)
        self.y1 += d_y1 * self.dt
        self.y2 += d_y2 * self.dt
        self.y3 += d_y3 * self.dt

        summing = self.y1 + self.y2 + self.y3
        self.y1 = self.y1 / summing
        self.y2 = self.y2 / summing
        self.y3 = self.y3 / summing

    def run(self) -> None:
        """Runs the simulation and reproduction for given amount of iterations."""
        for _ in tqdm(range(self.iters)):
            self.history['y1'].append(self.y1)
            self.history['y2'].append(self.y2)
            self.history['y3'].append(self.y3)
            self.step()

    def plot(self) -> None:
        """Displays population proportions as a function of time."""
        # set up plot
        plt.figure()
        plt.plot(range(self.iters), self.history['y1'], label='Citizens')
        plt.plot(range(self.iters), self.history['y2'], label='Trustworthy governors')
        plt.plot(range(self.iters), self.history['y3'], label='Untrustworthy governors')

        # add labels and title
        plt.xlabel('Iter')
        plt.ylabel('Proportion')
        plt.title('N-player trust game simulation')
        plt.legend()

        plt.show()

    
        plt.figure()
        triangle_points = [[0, 0], [1, 0], [0.5, math.sqrt(3) / 2]]

        # Plot triangle
        for i in range(3):
            start, end = triangle_points[i], triangle_points[(i + 1) % 3]
            plt.plot([start[0], end[0]], [start[1], end[1]], 'k-')

        # Plot trajectory
        prev_x, prev_y = None, None
        for i in range(len(self.history['y1'])):
            x, y = simplex_map((self.history['y1'][i], self.history['y2'][i], self.history['y3'][i]))
            if i == 0:
                plt.plot(x, y, marker='.', color='violet')
                prev_x = x
                prev_y = y
            if i % 10 == 0 and i != 0:
                plt.arrow(prev_x, prev_y, x - prev_x, y - prev_y, head_length=0.05, head_width=0.03, color='violet')
                prev_x = x
                prev_y = y

        plt.title('Simplex Plot')
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()

# Set up cmd line args
parser = argparse.ArgumentParser(prog='N-player trust game replicator dynamics simulator', description='Simulates the N-player trust game')
parser.add_argument('--y1', type=float, help='Proportion of citizens')
parser.add_argument('--y2', type=float, help='Proportion of trustworthy governors')
parser.add_argument('--y3', type=float, help='Proportion of untrustworthy governors')
parser.add_argument('--tv', type=float, help='Trusted value; how much a citizen pays')
parser.add_argument('--iters', type=int, help='Number of rounds in simulation')
parser.add_argument('--R1', type=float, help='Constant for trustworthy governors')
parser.add_argument('--R2', type=float, help='Constant for untrustworthy governors')
parser.add_argument('--dt', type=float, help='Timestep size for using replicator differential equation, defaults to 0.01')

def main():
    args = parser.parse_args()
    simulator = Simulator(args.y1, args.y2, args.y3, args.tv, args.R1, args.R2, args.iters)
    
    simulator.run()
    simulator.plot()

if __name__ == '__main__':
    main()
