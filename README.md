# N-Player Trust Game Simulator
Simulator of the N-Player Trust Game, introduced by Abbass et al [1].

## Dependencies
Run `pip install -r requirements.txt`.

## Simulating the game
Run `python simulatior.py --y1=y1 --y2=y2 --y3=y3 --tv=tv --iters=iters --R1=R1 --R2=R2 [--dt=dt]`, where `y1` is the proportion of citizens, `y2` the proportion of trustworthy governors, `y3` the proportion of untrustworthy governors, `pop_size` the total number of players, `tv` the trusted value (how much a citizen pays), `iters` the number of rounds in the simulation, `R1` the constant for trustworthy governors, and `R2` the constant for untrustworthy governors. `dt` is optional and will default to `0.01`.

[1] Abbass, H., Greenwood, G., & Petraki, E. (2016). The N-Player Trust Game and its Replicator Dynamics. IEEE Transactions on Evolutionary Computation, 20(3), 470-474.