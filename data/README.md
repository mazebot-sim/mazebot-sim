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
| Speed per PWM | 3.68 mm/s × (PWM − 9) | measured 2026-11-17 at PWM 90 (1 m in 3.35 s) and 255 (2 m in 2.21 s) | `speed_slope`, `pwm_start` |
| Slide when rotating on the spot | ~5 cm to the right per half turn | tape-cross test 2026-11-19, before the 10 % trim | `rotation_left_gain` (not fitted yet) |
| Sensor lag | ~150 ms | estimated from turn tests 2026-11-18 | `sensor_lag`; with Sensormodul's code in the loop it becomes a check, not an input |
| Roll-out, braking | 70 ms, 160 ms | measured at Läge B 2026-11-18 | `coast_tau` (roll-out) |
| Side IR range | 4–27 cm, outside = "no wall" | data sheet and the team's linearisation | `ir_short_range` |
| Front IR range | 20–150 cm | data sheet | `ir_long_range` |
| Gyro drift | −2°/min | drift test 2026-11-19 | `gyro_drift_dps` |
| Control rate | 40 Hz (25 ms) | Styrmodul firmware | `tick` |
| Corridors | 40 ± 2 cm wide, a tree, 90° turns | track specification 2.8–2.10 | `maze.CELL` = 40 cm; random width planned |

## Still to measure

In order of importance. Note the battery voltage at every measurement: speed
depends on it.

| # | What | How | Feeds |
|---|---|---|---|
| A1 | Fork reach from the centre | Ruler, centre to fork tip | `front_reach`, collisions |
| A2 | Rear reach from the centre | Ruler, centre to the rearmost point | `rear_reach`, collisions in turns |
| A3 | Position and angle of each IR sensor, and of the 11 tape detectors | Ruler from the centre | Sensor rays, tape model |
| B1 | Speed at more PWM values | Time 1 m at PWM 40, 60, 150, 200; find the lowest PWM that moves | Is the speed line straight? Real `pwm_start` |
| B2 | Acceleration from standstill | Film a start at PWM 90 and 255 next to a ruler | `accel_tau` |
| C1 | Rotation rate on the spot | Time 3 full turns at PWM 100 and 145, both directions | `track_width_eff` |
| C2 | Slide in a half turn with the 10 % trim | Tape-cross test again | `rotation_left_gain` |
| C3 | Gyro scale | Turn exactly 5 turns by hand on a tape mark, compare with the gyro | Gyro model |
| S1 | IR raw readings vs distance | Each sensor against a wall every 2 cm; 50 readings each | Sensor curve and noise |
| S2 | Gyro standing still | Log 5 minutes | Noise; checks the drift |
| S3 | Tape sensor at the goal T | How far onto the T before the robot sees it | Tape model |
| T1 | Track details | Exact corridor width, wall thickness, goal table size and position | Maze geometry |
| V1 | Validation runs | Telemetry log plus video from above: Läge A, B, C; a straight corridor at PWM 90 and 255; two whole mazes | Milestone 3 |

## Files

Name files by date and content, e.g. `2026-11-25_turn360.csv`. Videos are too
large for git: put them in a GitHub Release or a shared folder and link them
here.

| File | Date | What, and how it was measured | Used for |
|---|---|---|---|
