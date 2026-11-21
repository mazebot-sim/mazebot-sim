# Design

How the simulator works, from a random maze to a result, and how we build
it. The tasks are in [`PLAN.md`](PLAN.md); choices still open are at the end
of this file.

## One run

A run puts the simulated robot at the entrance of a maze, presses Start, and
lets the real firmware drive until it is back out with the object, fails, or
runs out of time. Everything else (validation, statistics, tuning, learning)
is many runs.

```
                 ┌──────────────── simulated world (Python) ────────────────┐
  Maze ─walls──► │  Sensor physics            Motion model                  │
                 │  IR: ray → ADC value       PWM + DIR per side → x, y, θ  │
                 │  gyro: rate → raw LSB              ▲                     │
                 │  tape: detectors over T            │                     │
                 └────────┬───────────────────────────┼─────────────────────┘
                          │ raw readings              │ motor_output_t, fork
                          ▼                           │
       Sensormodul logic (C, 50 Hz)          Styrmodul logic (C, 40 Hz)
       filter, linearise, angle, tape  ──►   state_machine_step()
                          │   telemetry           ▲
                          └──► Pi link (50 Hz) ───┘
```

The two C boxes are the robot's own code, unchanged. The simulator replaces
what is around them: the hardware, the Pi's forwarding, and the world.

## The parts

### Maze (`mazesim/maze.py`, exists)

Random mazes following the track rules: 40 cm cells (corridor width
random per maze, 38–42 cm), a tree, at most one
four-way crossing, the goal at a dead end. A seed gives the same maze every
time. Walls are line segments.

### Motion model (`mazesim/robot.py`, exists)

Each side follows its commanded speed (from the measured speed line) with a
first-order lag; rotation on the spot can slide sideways. Collision: the
robot's outline (a rectangle from `params.py`) against the wall segments.

### Sensor physics (`mazesim/sensors.py`)

The simulator produces what the sensor board's ADC and gyro would read, not
finished centimetres, so Sensormodul's real filtering and linearisation run
on them and the lag appears by itself instead of being a fitted 150 ms.

- **IR:** a ray from each sensor's position (A3) to the nearest wall, turned
  into an ADC value by the sensor's curve, plus noise. First version: the
  inverse of Sensormodul's own calibration tables; later, the curve measured
  in S1. Each sensor holds its value between its own measurements
  (GP2Y0A41: ~16 ms, GP2Y0A02: ~38 ms, data sheets).
- **Gyro:** the true turn rate in raw units (15.625 mdeg/s per LSB), plus a
  bias that drifts (−2°/min) and noise (S2), and a scale error (C3). The run
  starts with the robot standing still for 2 s, as on the robot, so the
  firmware calibrates the bias.
- **Tape:** 11 detectors (positions from A3) over the floor; a detector over
  the goal T reads high, otherwise low.

### Firmware in the loop (`firmware/`, `mazesim/firmware.py`)

- `firmware/vendor/` holds a copy of `styrmodul/logic`, `sensormodul/logic`
  and `protocol` from the course repository; `firmware/README.md` records the
  commit and `firmware/update.sh` copies a newer one.
- `firmware/sim_api.c` is a thin layer with a few plain functions, so Python
  never needs to know the layout of the C structs:
  `sim_new()`, `sim_free()`, `sim_start(speed)`,
  `sens_step(raw readings) → telemetry`,
  `ctrl_receive(telemetry)`, `ctrl_step() → motors, fork, state`.
  It does what the two `main.c` files do around the logic, and nothing more;
  compare them when updating the vendored copy.
- `firmware/Makefile` builds one shared library (`.dylib` on macOS, `.so` on
  Linux) with plain `cc`. `mazesim/firmware.py` loads it with `ctypes`.
- Many robots can run in one process: all firmware state lives in structs,
  none in globals.

### Timing (`mazesim/sim.py`)

An integer clock in steps of 5 ms, so every rate is exact:

| What | Every | Note |
|---|---|---|
| Motion model, collisions | 5 ms | |
| Sensormodul | 20 ms | |
| Pi reads Sensormodul, writes Styrmodul | 20 ms | |
| Styrmodul `state_machine_step()` | 25 ms | |

The three boards run on their own clocks, so each run starts them at random
offsets from each other (from the run's seed). Sensor lag then varies from
run to run as it does on the robot.

### Competition rules the simulator follows

From the course's *Ban- och tävlingsspecifikation* ver 0.1 (section numbers
in brackets). Version 0.1 is not approved yet; check for a newer one.

- Corridors 40 ± 2 cm [2.9]: each maze gets a random width in that range.
  A tree [2.8], 90° turns only [2.10], at most one four-way crossing [2.11].
- The robot starts wholly behind the start line, pointing in [4.1].
- The object sits on a table in the middle of a dead end, the same distance
  from three walls [3.3]; the T points at it, centred, a fork's length away
  [3.5, 3.6].
- **Timed** from the moment the fork alone holds the object up [4.2, 4.3]
  until the whole robot has passed the finish line [4.4]. The search is not
  timed, but the whole attempt may take at most 10 minutes [4.5].
- **+5 s each time the robot or the object touches a wall** [5.4]. The rule
  does not limit this to the return, so touches during the search count too.
- Dropping the object makes the attempt invalid [5.5].

### Wall contact

A touch is a penalty, not the end of the run, so the simulator has to let
the robot carry on after one, as on the track:

- The robot's outline, plus the fork and object once lifted, is checked
  against the walls every 5 ms.
- On contact the robot is pushed back out of the wall and its speed into the
  wall is removed, so it slides along it. Crude, but enough to see whether
  the firmware recovers; the scraping itself is not validated.
- A **touch** is counted when contact starts after at least 0.5 s without
  contact, roughly how a judge would count "each time".
- A robot pressed against a wall without moving for 5 s is **stuck**, and
  the run ends.

### The result of a run (`mazesim/sim.py`)

`run(maze, seed, params, trace=False) → RunResult`:

- **outcome:** `finished`, or why not: `stuck`, `lost` (the firmware
  stopped: lost, turn limit), `dropped` (fork lowered while carrying), or
  `timeout` (10 minutes)
- **score**, as the competition counts it: timed return + 5 s × touches;
  only for `finished`
- **touches** (search and return separately), timed return, search time,
  closest distance to a wall
- **trace**, only when asked for: position, heading, telemetry, motors and
  state every tick

### Fast without graphics, a viewer to watch

The simulator core (`mazesim/`) never imports matplotlib; batches, tuning
and training run without drawing and without a trace. What keeps it fast:

- **Only nearby walls** go into the ray and collision checks (a lookup by
  cell), not all of the maze's walls. Rays are the most frequent work.
- **One run per core** (`multiprocessing`), the same seeds for every
  comparison.
- **Stop early:** a run ends as soon as its outcome is known.
- **Measure before optimising:** `cProfile` on one run. If Python is still
  too slow, the motion and ray code moves to C next to the firmware.

To watch a result, `experiments/view.py` reruns one maze with the trace on
and animates it (matplotlib): the maze, the robot outline, the sensor rays,
the firmware state and the path, with pause and step. A run is fully decided
by its maze seed, run seed and parameters, so anything from a batch, a
tuning result or a trained policy can be replayed exactly without saving
traces; `--save run.mp4` writes a video instead.

## Validation (milestone 3)

1. Log the robot on the track: telemetry from the GUI plus a video from
   above. The GUI does not log to file yet; adding a CSV log comes first.
2. Rebuild the logged track as a maze, start the simulator in the same place,
   and run.
3. Compare: where it stopped before walls and at openings, angles after
   turns, offset from the centreline in corridors, the telemetry itself.
4. Fit the guessed parameters (`accel_tau`, `track_width_eff`,
   `rotation_left_gain`, sensor noise) until it agrees, and report what
   still does not, in numbers.

## Many runs (milestones 4–6)

- **Batch** (`experiments/batch.py`): the same N mazes and seeds for every
  comparison, one process per core, results to `runs/` as CSV. Output: share
  of finished runs, score, wall touches, and why the others failed.
- **Tuning** (`experiments/tune.py`): the firmware's `#define`s become
  compile-time options (`-DSM_APPROACH_CM=55`; `update.sh` wraps each in
  `#ifndef` when it copies the code), one library per parameter set, cached
  by its values. An optimiser (Optuna) picks the values; the
  score is the competition score over the batch, with failed runs counted
  as a large penalty.
- **Learning** (`experiments/train.py`, bonus): a Gymnasium environment
  around the run. The policy replaces only the corridor steering (the PID),
  while the state machine still navigates, so it can be compared with the
  PID on the same batch. Stable-Baselines3 (PPO) on the CPU.

## Layout

```
mazesim/
  params.py     measured parameters, each with its source (exists)
  maze.py       maze generator (exists)
  geometry.py   rays and segments (exists)
  robot.py      motion model and outline (exists)
  sensors.py    IR, gyro, tape: world to raw readings
  firmware.py   ctypes wrapper of the firmware library
  sim.py        the clock, run(), RunResult
  plot.py       plots and animation
firmware/
  vendor/       copy of the robot's logic and protocol
  sim_api.c     the layer Python calls
  Makefile, update.sh, README.md
experiments/    validate.py, batch.py, tune.py, train.py, view.py
data/           measurements (see data/README.md)
runs/           output, ignored by git
tests/
```

## Open decisions

When decided, move it to [`decisions.md`](decisions.md).

1. **Telemetry rate for validation.** The GUI receives 10 Hz. Enough for
   positions (the video gives those), thin for turns. *Decide after the
   first logged run* whether a faster log is needed.
