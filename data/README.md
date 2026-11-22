# Measurements

Everything known about the real robot and the track, and what is still to be
measured. `mazesim/params.py` holds the values the simulator uses; this file
says where they come from.

## What we have

| Quantity | Value | Source | In `params.py` |
|---|---|---|---|
| Robot width, length | 20 cm, 26.5 cm with fork | measured 2026-11-18 | `width`, `length_with_fork` |
| Fork reach from the centre | ~16.5 cm | estimate, **measure (A1)** | `front_reach` |
| Front sensor ahead of the centre | 10 cm | measured 2026-11-18 | `front_sensor_ahead` |
| Speed per PWM | 3.68 mm/s × (PWM − 9) | derived from two points measured 2026-11-17: PWM 90, 1 m in 3.35 s; PWM 255, 2 m in 2.21 s (`2026-11-17_speed_flying_start.csv`). Two points only: B1 checks the line | `speed_slope`, `pwm_start` |
| Straight-line pull | slight drift to the right at equal PWM, visible over a few metres | observed 2026-11-19, not measured | none yet |
| Slide when rotating on the spot | ~5 cm to the right per half turn, either direction | tape-cross test 2026-11-19, before the 10 % trim; with the trim "much better", not measured (C2) | `rotation_left_gain` (not fitted yet) |
| Rotation rate | PWM 255 turned too far past 90°, 145 fine, 100 slow; at PWM 100 one 90° left turn reached only ~70° in 2 s (2026-11-13, cause not checked) | observations 2026-11-13 to 11-17, not measured (C1) | `track_width_eff` is a guess; the 2 s observation suggests it may be far off |
| 180 in a dead end | arrived ~20° askew from zigzag, 3-7 cm off centre; the rear wheel hit the right wall rotating left, the fork the right wall rotating right | 2026-11-18 and 11-19, `2026-11-18_dead_end_180.csv` | validation (V1) |
| Sensor lag | ~150 ms | estimate (moving average, Pi forwarding, confirmation ticks), set 2026-11-17, never measured on its own | `sensor_lag`; with Sensormodul's code in the loop it becomes a check, not an input |
| Roll-out | 70 ms (~2 cm at PWM 90) | **guess** in the firmware (`SM_OPENING_ROLLOUT_MS`), not measured | `coast_tau` |
| Braking from PWM 255 to 90 | 160 ms × the speed shed | derived 2026-11-18 from Läge B: 6, 12, 11 cm past at PWM 255 (`2026-11-18_opening_stop_offsets.csv`) | none yet |
| Where a side opening is seen | when the robot's centre is at the opening's near corner | 2026-11-17, robot pushed by hand past an opening, GUI read: the side sensors sit at the chassis centre | sensor positions (A3) |
| Stop position at openings | at PWM 90 with the way ahead open, 6 cm past the middle, three of three (2026-11-19); with a wall ahead spot on | `2026-11-18_opening_stop_offsets.csv` | validation (V1) |
| Side IR range | 4–27 cm, outside = "no wall" | data sheet and the team's linearisation | `ir_short_range` |
| Front IR range | two sensors: front-left short range 4–27 cm decides below 20 cm, front-right long range 20–150 cm otherwise | data sheet, Sensormodul's `linearise_front()` | `ir_short_range`, `ir_long_range` |
| Gyro drift | −2°/min, steady | one run standing still for 5 min, 2026-11-19 (`2026-11-19_gyro_drift_standstill.csv`) | `gyro_drift_dps` |
| Gyro scale | a hand-turned 180° read 184.6° | one reading by eye, 2026-11-18; within reading error (C3 measures it) | none yet |
| Fork | servo pulse 1000 µs lowered to 2000 µs raised; lifting at full servo speed right after stopping tipped the table, 1 s wait and a 2 s lift did not | firmware `gripper.h`; observed 2026-11-20 | fork model (later) |
| Backing off the goal table | 5 cm still hit the table when turning round; 13 cm chosen, not yet confirmed | 2026-11-20 | goal manoeuvre (later) |
| Control rate | 40 Hz (25 ms) | Styrmodul firmware | `tick` |
| Corridors | 40 ± 2 cm wide, a tree, 90° turns | track specification 2.8–2.10 | `maze.CELL` = 40 cm; random width planned |

## Still to measure

In order of importance. Note the battery voltage at every measurement: speed
depends on it.

| # | What | How | Feeds |
|---|---|---|---|
| A1 | Fork reach from the centre | Ruler, centre to the fork tip and its outer corners | `front_reach`, collisions |
| A2 | Rear reach from the centre | Ruler, centre to the rearmost point and each wheel's outer corner | `rear_reach`, collisions in turns |
| A3 | **L1** Position and angle of each IR sensor, and of the 11 tape detectors | Ruler from the centre; check the side sensors' set-back in a corridor against the GUI | Sensor rays, tape model |
| A4 | Weight with and without the object; the object's size | Kitchen scale, ruler | Motion with the object (later) |
| B0 | Reference run, every driving session | PWM 90 over 1 m, 3 times, at the start and end of the session and every 20–30 min | How much the battery changed the speed during a session |
| B1 | **L1** Speed at more PWM values | Time 1 m (2 m from 150 up) at PWM 30, 40, 60, 90, 120, 150, 200, 255, 3 runs each; find the lowest PWM that moves | Is the speed line straight? Real `pwm_start`; the inner side when steering |
| B2 | **L1** Acceleration from standstill | Film a start at PWM 90 and 255 next to a tape measure, position every 0.1 s | `accel_tau` |
| B3 | Roll-out | Film a stop from PWM 90 and 255, position every 0.05 s | `coast_tau` |
| B4 | **L1** Pull to one side | Drive 3 m from a straight tape line with equal PWM, measure the offset, PWM 90 and 255 | Straight-line asymmetry |
| B5 | Battery effect | B1 at PWM 90 and 255 with a nearly flat battery | How much to randomise speed |
| C1 | Rotation rate on the spot | Time 3 full turns at PWM 100 and 255 (manual), both directions | `track_width_eff` |
| C2 | Slide in a half turn with the 10 % trim | Tape-cross test again, both directions, with and without the object | `rotation_left_gain` |
| C3 | **L1** Gyro scale | Turn exactly 5 turns by hand on a tape mark, compare with the gyro | Gyro model |
| C4 | Autonomous turn accuracy | Real angle after the turn at Läge C (90°) and Läge A (180°) vs the GUI heading | Turn model, validation |
| D1 | **L1** Turning radius while driving | Drive a full circle left and right by hand (inner side at a third), PWM 90 and 255; measure the diameter and the time per circle | How much a difference between the sides turns the robot; whether the inner side stalls at PWM 30 |
| D2 | **L1** Smallest PWM difference that turns the robot | Temporary Styrmodul build: left at 90 − X, right at 90, X = 5–40; drive 2 m, measure the sideways offset | The firmware's dead band (`PID_STEER_MIN`, a guess); the level 1 policy's steering |
| S1 | **L1** Side IR reading vs distance | Each side sensor against the track's cardboard from 4 to 30 cm in 2 cm steps; lowest and highest GUI value over ~5 s | Sensor curve and noise |
| S1b | **L1** Side IR at an angle | As S1, cardboard turned 0°, 15°, 30°, 45° at 10 and 20 cm | Sensor error when the robot points askew |
| S2 | **L1** Gyro standing still | Heading every 30 s for 5 min, 3 power-ons | Noise; checks the drift |
| S3 | Tape sensor at the goal T | How far onto the T before the robot sees it; what the start line shows | Tape model |
| T1 | **L1** Track details | Exact corridor width, wall thickness, goal table size and position | Maze geometry |
| V1 | Validation: manoeuvres | Telemetry log plus video from above: Läge A, B, C at PWM 90 and on the way back at 255 | Milestone 3 |
| V2 | **L1** Validation: straight corridor | Video from above of a 2 m corridor at PWM 90 and 255 with today's PID; offset from the middle every 20 cm | The zigzag to reproduce; the baseline for level 1 |
| V3 | Validation: whole mazes | Two whole mazes, search and way back, every wall touch noted | Milestone 3 |

**L1**: needed for level 1, the learned corridor steering. How to do each one
is in [`PROTOCOL.md`](PROTOCOL.md); empty files to fill in are in
[`templates/`](templates/).

## Files

Name files by date and content, e.g. `2026-11-25_turn360.csv`. Videos are too
large for git: put them in a GitHub Release or a shared folder and link them
here.

| File | Date | What, and how it was measured | Used for |
|---|---|---|---|
| `2026-11-17_speed_flying_start.csv` | 2026-11-17 | Steady speed at PWM 90 and 255, three runs each, stopwatch | `speed_slope`, `pwm_start` |
| `2026-11-18_opening_stop_offsets.csv` | 2026-11-18, 11-19 | Stop position before right turns at Läge B and C, ruler against a tape mark | Validation; firmware's opening constants |
| `2026-11-18_dead_end_180.csv` | 2026-11-18 | Side distances, heading and skew before and after the 180 at Läge A | Validation; turn model |
| `2026-11-19_gyro_drift_standstill.csv` | 2026-11-19 | Heading over 5 min standing still, read off the GUI | `gyro_drift_dps` |
