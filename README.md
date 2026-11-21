# mazebot-sim

A 2D simulator for a small autonomous maze robot, built to test, tune and
eventually train its controller off the robot, and to check the result back on
the real thing.

The robot (a course project, TSEA29 at Linköping University) explores a maze
of 40 cm cardboard corridors, finds a tape "T", lifts an object off a table
with a fork, and drives back to the entrance by the shortest route. Its
controller runs on an ATmega1284P. The robot's control logic
is copied into `firmware/vendor/` from the course repository, with the commit
it came from, so the simulator builds without access to that repository.

## Idea

1. **Model the robot from measurements** (system identification): speed per
   PWM, acceleration, roll-out, sideways slide when rotating on the spot,
   sensor ranges, noise and lag, gyro drift. Every value in
   `mazesim/params.py` says where it came from.
2. **Run the real firmware in the loop** (software-in-the-loop): the logic of
   both boards is plain C with no hardware access, so the simulator runs the
   same sensor processing and `state_machine_step()` the robot runs.
3. **Validate**: reproduce what was measured on the track before trusting
   anything else the simulator says.
4. **Tune and train**: optimise the controller's parameters over thousands of
   random mazes, then try a learned policy against the hand-tuned one.
5. **Back to the robot**: try the result on the real track and report the
   difference honestly.

## Status

Tasks, roles and how we work are in [`docs/PLAN.md`](docs/PLAN.md).

| Milestone | Goal | State |
|---|---|---|
| 1 | Maze generator, robot motion model, geometry | started |
| 2 | Sensors and the real firmware in the loop | |
| 3 | Validation against track measurements | |
| 4 | Statistics over many random mazes | |
| 5 | Parameter optimisation | |
| 6 | Reinforcement learning, compared with the PID | |
| 7 | Write-up: graphs, side-by-side video | |

## Setup and tests

Python 3.12, managed with [uv](https://docs.astral.sh/uv/) so everyone gets
the same versions (`brew install uv` on macOS):

```
uv sync                                          # creates .venv from uv.lock
uv run python -m unittest discover -s tests -t .
```

Add a dependency with `uv add <package>` and commit `pyproject.toml` and
`uv.lock` together.

## Layout

```
mazesim/       the simulator (maze, geometry, robot model, parameters)
firmware/      building the robot's control logic as a library (milestone 2)
experiments/   validation, batch runs, tuning, training
data/          measurements from the real robot
docs/          the plan, the design and the decision log
tests/         unit tests
```
