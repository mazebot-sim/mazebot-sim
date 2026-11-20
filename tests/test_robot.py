import math
import unittest
from dataclasses import replace

from mazesim import robot
from mazesim.params import G05
from mazesim.robot import FORWARD, BACKWARD, RobotState


def run(state, cmd, seconds, p=G05):
    for _ in range(round(seconds / p.tick)):
        state = robot.step(state, *cmd, dt=p.tick, p=p)
    return state


class TestRobot(unittest.TestCase):
    def test_speed_matches_measurements(self):
        # Measured 2026-11-17: 0.298 m/s at PWM 90, 0.905 m/s at PWM 255.
        self.assertAlmostEqual(robot.pwm_to_speed(90), 0.298, places=3)
        self.assertAlmostEqual(robot.pwm_to_speed(255), 0.905, places=3)
        self.assertEqual(robot.pwm_to_speed(5), 0.0)

    def test_straight_at_pwm_90_settles_at_measured_speed(self):
        s = run(RobotState(), (90, FORWARD, 90, FORWARD), 2.0)
        self.assertAlmostEqual(s.v_left, 0.298, places=2)
        self.assertAlmostEqual(s.y, 0.0, places=9)        # straight along +x
        self.assertAlmostEqual(s.theta, 0.0, places=9)

    def test_coasts_to_a_stop(self):
        s = run(RobotState(v_left=0.3, v_right=0.3), (0, FORWARD, 0, FORWARD), 1.0)
        self.assertLess(abs(s.v_left), 0.001)
        self.assertLess(s.x, 0.05)                         # a few cm of roll-out

    def test_rotation_on_the_spot_stays_put_without_asymmetry(self):
        s = run(RobotState(), (100, BACKWARD, 100, FORWARD), 1.0)
        self.assertGreater(s.theta, 0.5)                   # turned left
        self.assertLess(math.hypot(s.x, s.y), 1e-9)

    def test_rotation_asymmetry_makes_it_slide(self):
        p = replace(G05, rotation_left_gain=1.2)
        s = run(RobotState(), (100, BACKWARD, 100, FORWARD), 1.0, p)
        self.assertGreater(math.hypot(s.x, s.y), 0.005)


if __name__ == "__main__":
    unittest.main()
