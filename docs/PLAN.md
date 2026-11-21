# Plan

The one plan we both follow. If it is not in this file, it is not planned.

## How we work

- **Tasks** are the checkboxes below. Put your initials on a task before
  starting it, so we never both do the same thing: `- [ ] (JG) ...`.
- **One branch and one pull request per task.** The other person reviews and
  merges. Tick the box in the same pull request that does the work.
- **Decisions** (a choice someone would otherwise ask about later) go in
  [`decisions.md`](decisions.md), one line each.
- **Measurements** from the robot go in `data/`, listed in
  [`data/README.md`](../data/README.md).
- **Experiment output** (batch runs, checkpoints, videos) goes in `runs/`,
  which git ignores. Copy what is worth keeping to `data/` or `docs/`.
- **Weekly check-in** of 15 minutes: what got done, what is next, what is
  blocking. Update this file during it.

Roles, so the work can run in parallel (swap at least once):

- **A, physics and validation:** sensor and motion models, fitting to `data/`.
- **B, firmware and tools:** firmware in the loop, simulation loop, plots, CI.

## Now: measure the robot while we have it

Only possible while the course runs. Comes before everything else. What we
already have, and how to measure each item, is in
[`data/README.md`](../data/README.md).

- [ ] A1–A3: fork reach, rear reach, sensor positions
- [ ] B1: speed at more PWM values, and the lowest PWM that moves
- [ ] B2: start from standstill at PWM 90 and 255
- [ ] C1: rotation rate on the spot, both directions
- [ ] C2: slide in a half turn with the 10 % trim
- [ ] C3: gyro scale over 5 turns
- [ ] S1: IR raw readings vs distance
- [ ] S2: gyro standing still for 5 minutes
- [ ] S3: where on the goal T the tape sensor triggers
- [ ] T1: track details
- [ ] Add a CSV telemetry log to the course GUI (needed for V1)
- [ ] V1: logged validation runs with video

## Milestones

### 1. Maze, geometry, motion model

Done when: a robot can drive a commanded path through a random maze and the
simulator reports when it touches a wall.

- [x] Maze generator following the track rules
- [x] Ray and segment geometry
- [x] Motion model from the measured speed line
- [ ] Random corridor width 38–42 cm per maze; goal table and T in the
      maze (track rules 2.9, 3.3–3.6)
- [ ] Collision between the robot's outline and the walls; push-out,
      touch counting, stuck detection
- [ ] Plot of a maze with a driven path

### 2. Sensors and the real firmware in the loop

Done when: the real `state_machine_step()` drives a simulated robot through a
whole maze, shown as a GIF in the README.

See [`DESIGN.md`](DESIGN.md) for how these fit together.

- [x] Python 3.12 with `uv`
- [x] Decide the open questions at the end of `DESIGN.md`
- [ ] Copy `styrmodul/logic`, `sensormodul/logic` and `protocol` into
      `firmware/vendor/`, with the commit hash in `firmware/README.md`
- [ ] `firmware/sim_api.c` and `firmware/Makefile`: one shared library
- [ ] `mazesim/firmware.py`: load it with `ctypes`
- [ ] IR sensor physics: rays, ADC curve from the calibration tables, noise
- [ ] Gyro physics: raw rate, drifting bias, noise
- [ ] Tape detectors over the goal T
- [ ] `mazesim/sim.py`: the 5 ms clock, `run()`, `RunResult`
- [ ] `experiments/view.py`: replay a run with graphics, `--save` to GIF/MP4
- [x] CI on GitHub: ruff, tests, coverage
- [ ] CI: add the firmware build

### 3. Validation against the track

Done when: a short report shows, per logged run, where the simulator agrees
with the robot and where it does not, in numbers.

- [ ] Replay the logged runs in the simulator
- [ ] Fit the guessed parameters to the measurements
- [ ] Report: stop positions, turn angles, corridor offset, sim vs real

### 4. Statistics over many mazes

Done when: one command runs 1000 random mazes and prints success rate, time
and wall touches.

- [ ] Headless batch runner using all cores, with a fixed seed per run
- [ ] Summary table and plots of the results

### 5. Parameter optimisation

Done when: tuned parameters beat the hand-tuned ones over the batch, and we
know by how much.

- [ ] Choose the parameters and the score (time, wall touches, failures)
- [ ] Optimiser run, and a comparison with the robot's current values

### 6. Reinforcement learning (bonus)

Only once 1 to 5 are done.

- [ ] Gym environment around the simulator
- [ ] Train a policy and compare it with the PID over the same batch

### 7. Write-up

- [ ] README with GIF, results and how to run everything
- [ ] Side-by-side video, simulator and real robot
- [ ] Short report we can both link to from our CVs
