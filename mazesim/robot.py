"""The robot's motion: two wheel pairs (skid steering) driven by PWM and a
direction per side, as Styrmodul's motor_output_t.

Each side's speed follows its commanded speed with a first-order lag:
accel_tau while driving, coast_tau when the PWM is 0 (the motors coast). The
commanded speed comes from the measured speed line. Rotating on the spot, the
left side can be made to get further than the right (rotation_left_gain), the
skid asymmetry that made the robot slide sideways in a half turn.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from .params import G05, RobotParams

FORWARD, BACKWARD = 1, 0   # DIR_FORWARD, DIR_BACKWARD in styrmodul/logic/drive.h


@dataclass
class RobotState:
    x: float = 0.0          # chassis centre, metres
    y: float = 0.0
    theta: float = 0.0      # heading, radians, counter-clockwise from +x
    v_left: float = 0.0     # side speeds, m/s, forward positive
    v_right: float = 0.0


def pwm_to_speed(pwm: int, p: RobotParams = G05) -> float:
    """Steady speed in m/s for a PWM 0..255, from the measured line."""
    return max(0.0, p.speed_slope * (pwm - p.pwm_start))


def _approach(v, target, tau, dt):
    return target + (v - target) * math.exp(-dt / tau)


def step(state: RobotState, left_pwm: int, left_dir: int, right_pwm: int, right_dir: int,
         dt: float, p: RobotParams = G05) -> RobotState:
    """Advances the robot by dt seconds under one motor command."""
    tl = pwm_to_speed(left_pwm, p) * (1 if left_dir == FORWARD else -1)
    tr = pwm_to_speed(right_pwm, p) * (1 if right_dir == FORWARD else -1)
    vl = _approach(state.v_left, tl, p.accel_tau if left_pwm else p.coast_tau, dt)
    vr = _approach(state.v_right, tr, p.accel_tau if right_pwm else p.coast_tau, dt)

    gl = vl
    if vl * vr < 0:          # rotating on the spot: the skid asymmetry
        gl = vl * p.rotation_left_gain
    v = (gl + vr) / 2
    omega = (vr - gl) / p.track_width_eff

    th = state.theta + omega * dt / 2      # midpoint heading
    return RobotState(
        x=state.x + v * math.cos(th) * dt,
        y=state.y + v * math.sin(th) * dt,
        theta=state.theta + omega * dt,
        v_left=vl,
        v_right=vr,
    )
