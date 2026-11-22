# Templates

Empty measurement files for the level 1 measurements in
[`../PROTOCOL.md`](../PROTOCOL.md): the columns, and the rows already laid
out where the protocol fixes them (each PWM, each distance, each run). Only
the numbers are missing.

Each template asks only for the conditions that change its result:

- **battery** (and floor and load, which default to lab and none): driving
  measurements, since speed depends on the battery
- **Sensormodul's commit**: sensor measurements, since its linearisation and
  gyro code decide what the GUI shows
- **both commits and the PID gains**: V2, which runs the firmware itself

The date is in the file name. Who measured is not recorded.

`B0_reference_run.csv` goes with every session that drives the robot: a
short run at PWM 90 at the start, every 20–30 minutes, and at the end, to see
how much the battery has changed the speed.

To use one: copy it to `data/` with the date in front
(`2026-11-25_B1_speed_per_pwm.csv`), fill in the `#` lines and the empty
fields, and add it to the table in [`../README.md`](../README.md). Leave a
field empty if it was not measured; do not guess.
