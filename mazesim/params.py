"""The robot's measured parameters.

Every value says where it came from: "measured" with a date, "derived" from
measured values, or "guess" until measured (with the measurement that would
replace it). Lengths in metres, times in seconds, angles in radians unless the
name says otherwise.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class RobotParams:
    # --- Geometry, from the chassis centre (where the side sensors sit) ---
    width: float = 0.20               # measured 2026-11-18 (team)
    length_with_fork: float = 0.265   # measured 2026-11-18, rear to fork tip
    front_sensor_ahead: float = 0.10  # measured 2026-11-18
    front_reach: float = 0.165        # derived: 0.265 - rear reach; guess until A1
    rear_reach: float = 0.10          # guess: measure A2

    # --- Driving: speed = slope * (pwm - pwm_start), measured 2026-11-17 ---
    # PWM 90: 1 m in 3.35 s (0.298 m/s); PWM 255: 2 m in 2.21 s (0.905 m/s).
    speed_slope: float = 0.00368      # m/s per PWM step, derived from the two
    pwm_start: float = 9.0            # derived: the line meets zero speed here
    accel_tau: float = 0.15           # guess: measure B2 (start from standstill)
    coast_tau: float = 0.07           # derived: ~2 cm roll-out at 0.3 m/s (SM_OPENING_ROLLOUT_MS)

    # --- Rotating on the spot ---
    track_width_eff: float = 0.30     # guess: skid steering turns slower than the wheel
                                      # base suggests; measure C1 (time for 360 degrees)
    # The left side gets further than the right while skidding: the robot slid
    # ~5 cm to its right in any half turn (floor-cross test 2026-11-19, before
    # the 10 % trim). Fitted in milestone 3; 1.0 means no slide.
    rotation_left_gain: float = 1.0

    # --- Sensors ---
    ir_short_range: tuple = (0.04, 0.27)   # measured: GP2Y0A41SK0F, side and front-left
    ir_long_range: tuple = (0.20, 1.50)    # data sheet: GP2Y0A02YK0F, front-right
    sensor_lag: float = 0.15          # derived 2026-11-18 from the turn into Läge B
    gyro_drift_dps: float = -2.0 / 60  # measured 2026-11-19: -2 degrees a minute

    # --- Firmware timing ---
    tick: float = 0.025               # Styrmodul's 40 Hz step


G05 = RobotParams()
