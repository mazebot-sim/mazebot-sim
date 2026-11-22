# Measurement protocol

How to measure the robot so the simulator can be fitted to it. What each
measurement feeds and what is already known is in [`README.md`](README.md);
this file says exactly how, how often and in what form. The IDs (A1, B2 …)
are the same in both files.

The robot is only available while the course runs, so the sessions are
ordered to get the most out of each lab visit.

## What we measure for

The first learning goal is **level 1**: a trained policy replaces only the
corridor steering (the PID, `docs/decisions.md` 2026-11-21); the firmware
still does everything else. Level 1 needs the simulator to answer one
question well: *when the robot steers like this in a corridor, how does it
move, and what do its sensors see?* The measurements marked **L1** answer it,
and come first. The others make whole runs realistic (turns, the goal, the
way back) and come after.

| | Measurements |
|---|---|
| **Every driving session** | B0 reference run (the battery check) |
| **L1, how the robot responds to steering** | A3, T1, B4, B1, B2, D1, D2 |
| **L1, what the sensors see** | S1, S1b, S2, C3 |
| **L1, the answer to compare with** | V2 |
| Later, whole runs | A1, A2, A4, B3, B5, C1, C2, C4, S3, V1, V3 |

## Rules for every measurement

**Write down only the conditions that change the result** (the templates
ask for exactly these; the date is in the file name, who measured is not
recorded):

| Condition | For | Why |
|---|---|---|
| Battery voltage at the start and the end (a multimeter, or "fresh"/"used, about N minutes") | driving: B, D, V | speed depends on it by several per cent, and it cannot be recovered later |
| Floor, load (default: lab, none) | driving and rotation | only write them when they differ |
| Sensormodul's commit (`git log -1 --oneline` in `TSEA29projekt`) | sensors: S, C3, A3 check | its linearisation and gyro code decide what the GUI shows |
| Styrmodul's commit and the PID gains | V | the firmware drives |

Easiest: send the conditions once per session ("session 2, Styrmodul f664a58,
Sensormodul 9784db7, battery 7.9 V at start, 7.6 V at end"), and they go into
every file from that session.

**Reference run (B0) in every session with driving.** PWM 90, 1 m with a
run-up, 3 times, at the start and the end of the session, and every
20–30 minutes in between (or after about every 10 runs). It measures the one
thing the battery changes, the speed, and tells how much the session's
driving measurements must be corrected. If the time grows by more than 3 %
from the start (3.35 s to over 3.45 s), note it, and charge or change the
battery before measuring speed again. Template: `templates/B0_reference_run.csv`.

**Before each session**

- Charge the battery. Note the voltage at the start and the end.
- After flashing Styrmodul, click the GUI's speed button: a reset puts the
  robot back at PWM 90 without the GUI knowing.
- Power on and leave the robot untouched for 2 s, so the gyro calibrates.

**Record raw values, not averages.** One row per repetition. The spread is
part of the result: it says how much the simulator's parameters must be
randomised during training so a policy also works on the real robot.

**Repetitions** as given for each measurement, 3 at the very least. If one
repetition is far off the others, keep it and note why (wheel slipped, cable
caught …).

**Accuracy to aim for**

| Quantity | How | Aim |
|---|---|---|
| Lengths | steel ruler or tape measure | ±0.5 cm |
| Times | phone slow motion (240 fps), counting frames | ±0.01 s |
| Positions over time | slow-motion video beside a tape measure on the floor | ±1 cm |
| Angles | gyro in the GUI, or a line on the floor | ±2° |

**Video:** film from the side for straight driving, from above for turns.
Put a tape measure in the frame. Name the video like the data file and note
its frame rate. Videos stay out of git (see `README.md`).

## What the GUI cannot do yet, and how to get round it

- **Only PWM 90 and 255.** For other speeds, change `SPEED_NORMAL` in
  `TSEA29projekt/gui/ui/control_panel.py` on your own Mac, restart the GUI,
  measure, and undo it with `git checkout -- gui/ui/control_panel.py`. Never
  commit it. Manual rotation always runs at least PWM 100 (Styrmodul since
  2026-11-20).
- **No different PWM per side.** D2 needs a temporary Styrmodul build; see
  D2. Flash the normal firmware back afterwards, and never commit the test
  build.
- **No log to file.** Telemetry reaches the GUI at 10 Hz, as centimetres and
  degrees. Until a CSV log exists (task in `docs/PLAN.md`, a change in the
  course repository the team must agree to), read values off the screen, or
  film the screen next to the robot. The log would most improve V2, make V1
  and V3 possible, and save time in S1 and S2.
- **No raw sensor values.** The telemetry carries Sensormodul's linearised
  centimetres, not the ADC readings. S1 therefore measures the whole chain
  (sensor plus linearisation). Raw ADC values can be read with the debugger
  in Microchip Studio (`g_raw_adc` in Sensormodul's `main.c`) if needed later.

## File format

CSV, one file per measurement and day, named `YYYY-MM-DD_what.csv`, with the
conditions as `#` comments on top. Example:

```
# B1: steady speed per PWM, flying start
# battery: 7.9 V at start, 7.6 V at end   floor: lab   load: none
# how: 50 cm run-up; time from the front passing mark 1 to mark 2; 240 fps
pwm,run,distance_m,time_s
90,1,1.0,3.31
```

Add each file to the table at the end of `README.md` in the same pull request.

## Level 1 measurements

All positions are from the **chassis centre**, the point between the two
side sensors: x forward, y to the left, in cm.

### Session 1: geometry and corridor (no video, about 1 h)

#### A3. Side sensor positions (L1)

- **What:** where the left and right IR sensors sit on the robot and which
  way they point. The front sensors and the 11 tape detectors too, while
  the ruler is out.
- **Why:** on 2026-11-18 at Läge A, left + right + robot width came to
  about 45 cm in a corridor of 38–42 cm, so the sensors probably sit some
  way in from the chassis edge. The simulator must measure from exactly the
  right point, or the policy learns that it stands somewhere it does not.
- **Setup:**
  1. Ruler from the chassis centre to the face of each sensor, forward/back
     and sideways; note the direction it points.
  2. Check: stand the robot straight in a corridor, measure with the ruler
     from each chassis side to its wall, and compare with what the GUI
     shows. The difference is the sensor's set-back.
- **Count:** every sensor once; the check at 3 places in the corridor.
- **Columns:** `part,x_cm,y_cm,angle_deg`; check: `place,ruler_left_cm,ruler_right_cm,gui_left_cm,gui_right_cm`

#### T1. Corridor width (L1)

- **What:** the real width between the walls; wall thickness and height.
- **Why:** it sets what "the middle of the corridor" is. The rules say
  40 ± 2 cm, but the team's track may differ.
- **Setup:** tape measure at floor level, at the sensors' height, at
  several places along the corridors. Wall thickness and height once.
- **Count:** 5–10 places.
- **Columns:** `what,place,value_cm`

#### B4. Pull to one side (L1)

- **What:** how far the robot drifts to the right with the same PWM on both
  sides.
- **Why:** the PID corrects it all the time. If the simulator lacks it, the
  policy trains against a robot that drives straight, and does worse on the
  real one.
- **Setup:** a straight tape line, 3 m, on open floor. Stand the robot with
  its centre on the line, pointing along it. Drive straight forward by hand
  for 3 m. Measure how far the centre ends up from the line, and to which
  side. Also read the heading change in the GUI.
- **Count:** 5 at PWM 90, 5 at PWM 255 = 10.
- **Columns:** `pwm,run,distance_m,offset_cm,heading_change_deg` (offset + to the left)

### Session 2: speed and steering (slow motion, about 1.5–2 h)

#### B1. Speed at many PWM values (L1)

- **What:** speed in m/s at different PWM values, and the lowest PWM that
  moves the robot.
- **Why:** when the robot steers, one side runs slow (30–60) and the other
  fast. The speed line rests on PWM 90 and 255 only; near where the wheels
  stop it is probably wrong, and that is exactly where steering happens.
  If the simulator thinks a wheel turns at PWM 40 when it stands still, the
  policy learns to steer a robot that does not exist.
- **Setup:**
  1. Set `SPEED_NORMAL` in the GUI for each PWM (see above).
  2. Two tape marks 1 m apart (2 m from PWM 150 up), 50 cm run-up before
     the first.
  3. Film from the side in slow motion; time from the front passing the
     first mark to passing the second.
  4. **Lowest PWM:** from standstill, start at 10 and step up by 5 until the
     robot moves.
- **Count:** PWM 30, 40, 60, 90, 120, 150, 200, 255, 3 runs each = 24;
  5–10 tries for the lowest. Short of time: 30, 40, 60, 90, 120, 255.
- **Columns:** `pwm,run,distance_m,time_s`; lowest: `pwm,moved`

#### B2. Acceleration (L1)

- **What:** how fast the robot gets up to speed from standstill.
- **Why:** when the policy changes the steering, the wheels take a moment to
  follow. That lag must be in the simulator.
- **Setup:** tape measure along the floor, the robot standing at 0. Film
  from the side in slow motion and press forward. Read the front's position
  every 0.1 s for the first 1.5 s by counting frames.
- **Count:** 3 at PWM 90, 3 at PWM 255 = 6 videos.
- **Columns:** `pwm,run,t_s,x_cm`

#### D1. Turning radius while driving (L1)

- **What:** how tightly the robot turns when driven left or right by hand,
  which runs the inner side at a third of the speed.
- **Why:** it shows how much the heading changes for a given difference
  between the sides. The wheels slide sideways, so this cannot be worked
  out, only measured. At PWM 90 the inner side gets PWM 30, so it also shows
  whether that side stalls.
- **Setup:** open floor, at least 2 × 2 m. Drive left by hand one full
  circle. Mark the start point and the point farthest from it with tape; the
  distance between them is the diameter. Also time one circle, from video
  or the GUI heading.
- **Count:** left and right, at PWM 90 and 255, 3 each = 12.
- **Columns:** `pwm,direction,run,diameter_cm,time_one_circle_s`

#### D2. Smallest difference that turns the robot (L1)

- **What:** how large the PWM difference between the sides must be before
  the robot starts to turn.
- **Why:** the firmware's dead band (`PID_STEER_MIN`, 30 PWM steps) is a
  guess; its comment says "Measure PID_STEER_MIN on the floor". Below the
  threshold steering has no effect, and the policy must know where it is.
- **Setup:** the GUI cannot give the sides different PWM, so this needs a
  **temporary Styrmodul build** in which "left" gives PWM 90 − X on the left
  side and 90 on the right. Flash it, measure, flash the normal firmware
  back; never commit it. For each X drive 2 m straight from a tape line and
  measure how far the centre ends up to the side, compared with B4.
- **Count:** X = 5, 10, 15, 20, 30, 40, 2 runs each = 12. One flash per X,
  so allow extra time.
- **Columns:** `x_pwm,run,distance_m,offset_cm`

### Session 3: sensors and the answer to compare with (about 1.5 h)

#### S1. Side sensor reading vs real distance (L1)

- **What:** what the GUI shows with the wall at a known distance, and how
  much the value jumps.
- **Why:** the side distances are the policy's most important inputs. It
  must train on the same errors and noise as the robot has, or it gets
  confused on the real one.
- **Setup:** stand the robot firmly so it cannot move. A piece of the track's
  cardboard square in front of the sensor, moved from 4 to 30 cm in 2 cm
  steps. At each distance write the lowest and highest value the GUI shows
  over about 5 s.
- **Count:** 14 distances × 2 sensors = 28 points.
- **Columns:** `sensor,true_cm,min_cm,max_cm`

#### S1b. Side sensors at an angle (L1)

- **What:** what the sensor shows when the wall is not square to it.
- **Why:** when the robot zigzags it points askew, and then the sensors read
  a longer distance than the real one. That is exactly the situation the
  policy must learn to handle.
- **Setup:** as S1, with the cardboard turned 0°, 15°, 30° and 45° (a
  protractor or a printed angle template), at 10 cm and 20 cm.
- **Count:** 4 angles × 2 distances = 8 per sensor; one sensor is enough if
  time is short.
- **Columns:** `sensor,true_cm,angle_deg,min_cm,max_cm`

#### S2. Gyro standing still (L1)

- **What:** how the heading changes with the robot standing still.
- **Why:** the heading error is one of the policy's inputs. One run gave
  −2°/min (`2026-11-19_gyro_drift_standstill.csv`); this checks whether it
  is the same after every power-on.
- **Setup:** power on and do not touch the robot. Read the heading every
  30 s for 5 minutes. Do it while setting up something else.
- **Count:** 3 power-ons × 11 readings.
- **Columns:** `run,t_s,heading_deg`

#### C3. Gyro scale (L1)

- **What:** whether the gyro shows exactly 360° for one full turn.
- **Why:** if it reads, say, 2 % too much, the heading error the policy gets
  is a little wrong, and the error grows with every turn.
- **Setup:** a tape mark on the floor and one on the robot. Turn the robot
  by hand exactly **5 full turns** until the marks meet again. Read the
  heading before and after. Five turns make a small reading error matter
  less.
- **Count:** 3 left, 3 right = 6.
- **Columns:** `direction,run,turns,heading_before_deg,heading_after_deg`

#### V2. Straight corridor with today's steering (L1, the answer)

- **What:** how much the robot zigzags along a straight corridor with
  today's PID.
- **Why:** before trusting that the policy does better, the simulator must
  reproduce today's zigzag. It is also the baseline the policy is compared
  with.
- **Setup:** a straight corridor of at least 2 m. A phone high up, straight
  above, with the whole corridor in frame and tape marks every 20 cm along
  the wall. Drive through autonomously. From the video read the robot's
  distance from the middle at each mark. Film the GUI screen at the same
  time if possible.
- **Count:** 3 at PWM 90, 3 at PWM 255 = 6 runs.
- **Columns:** `pwm,run,mark_cm,offset_from_middle_cm,heading_deg`

### Level 1 summary

| Session | Measurements | Readings, about | Time |
|---|---|---|---|
| 1 | A3, T1, B4 | 25 | 1 h |
| 2 | B1, B2, D1, D2 | 60 | 1.5–2 h |
| 3 | S1, S1b, S2, C3, V2 | 60 | 1.5 h |

Plan a fourth session once the simulator runs: compare it with V2, see
where it differs most from the robot, and measure that.

### What level 1 is enough for

- **Enough:** training level 1 in the simulator; checking the simulator on
  straight corridors (V2); rough values for the rest, so whole mazes run.
- **Not enough:** trusting the simulator in turns, at openings and in dead
  ends (C1, C2, C4, V1, V3); the fork, the object and the T (A1, A2, S3);
  fast events without the telemetry log.

## Later measurements, for whole runs

Same rules as above.

### A. Geometry

| ID | What | Columns |
|---|---|---|
| A1 | Fork tip, and the fork's outer corners | `part,x_cm,y_cm` |
| A2 | Rearmost point, and each wheel's outer corner (front and rear, left and right) | `part,x_cm,y_cm` |
| A4 | Weight with and without the object, on a kitchen scale; the object's size | `what,value,unit` |

### B. Driving

| ID | What | How | Repeat | Columns |
|---|---|---|---|---|
| B3 | Roll-out | At steady PWM 90 and 255, press stop. Film from the side; read position every 0.05 s from 0.5 s before stop until still. Note the frame where the stop was clicked if the screen is in view | 3 per PWM | `pwm,run,t_s,x_cm` |
| B5 | Battery effect | B1 at PWM 90 and 255 with a nearly flat battery | 3 per PWM | as B1 |

### C. Rotating on the spot (open floor, tape cross)

| ID | What | How | Repeat | Columns |
|---|---|---|---|---|
| C1 | Rotation rate | Three full turns on the spot, time from slow-motion video from above (or the GUI heading). PWM 100 (GUI at 90) and 255, both directions | 3 per case | `pwm,direction,turns,time_s` |
| C2 | Slide in a half turn | Centre mark over a tape cross; half a turn; measure how far the centre moved, forward/back and left/right, in the robot's frame before turning. PWM 100, both directions, with and without the object | 5 per case | `pwm,direction,load,dx_cm,dy_cm` |
| C4 | Autonomous turn accuracy | Run into Läge C (90° turn) and Läge A (180°); after the turn, measure the real angle against the wall (ruler at two points) and read the GUI heading | 5 per place | `place,run,real_angle_deg,gui_heading_change_deg` |

### S. Sensors

| ID | What | How | Repeat | Columns |
|---|---|---|---|---|
| S3 | Tape sensor at the goal T | Push the robot slowly onto the T by hand; mark where the GUI first shows the goal (offset +127). Measure from that mark to the T's crossbar and to the table. Also: what the tape offset shows over the start line | 5 | `run,cm_before_crossbar,note` |

### V. Validation runs (autonomous, whole manoeuvres)

Needs the telemetry log, or at least film of the GUI screen in sync with the
robot. Film from above with the whole track in frame (a phone on a high
shelf or a tripod), four tape marks at known corners for scale.

| ID | What | Repeat |
|---|---|---|
| V1 | Läge A (180), Läge B (right, open ahead), Läge C (right, wall ahead), each at PWM 90 and on the way back at 255 | 3 each |
| V3 | Two whole mazes, search and way back, on the team's drawing; note every wall touch and where | 2 each |

For each run note: the firmware commits, the start position, the outcome,
and the time of each event (turn, lift, touch) from the video.

### Sessions for the later measurements

| # | Measurements | Needs |
|---|---|---|
| 4 | A1, A2, A4, B3, B5 (B5 at the end, when the battery is low) | Ruler, kitchen scale, phone |
| 5 | C1, C2, C4, S3 | Phone in slow motion, tape cross |
| 6 | V1, V3 | Camera from above; the telemetry log if it exists by then |
