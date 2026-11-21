"""Properties that must hold whatever the parameters: track rules over many
sizes, symmetry of the motion model, and independence of the time step."""
import math
import unittest

from mazesim import maze as mz
from mazesim import robot
from mazesim.robot import BACKWARD, FORWARD, RobotState


def drive(cmd, seconds, dt):
    s = RobotState()
    for _ in range(round(seconds / dt)):
        s = robot.step(s, *cmd, dt=dt)
    return s


class TestMazeInvariants(unittest.TestCase):
    def test_rules_hold_for_every_size(self):
        for cols in range(1, 9):
            for rows in range(2, 9):
                if cols == rows == 1:
                    continue            # one cell: no dead end for the goal
                for seed in range(20):
                    m = mz.generate(cols, rows, seed=seed)
                    self.assertEqual(mz.check_rules(m), [], f"{cols}x{rows} seed {seed}")

    def test_no_wall_segment_twice(self):
        for seed in range(50):
            segs = mz.generate(6, 5, seed=seed).wall_segments()
            normalised = [tuple(sorted(s)) for s in segs]
            self.assertEqual(len(normalised), len(set(normalised)), f"seed {seed}")


class TestMotionInvariants(unittest.TestCase):
    def test_backward_mirrors_forward(self):
        f = drive((150, FORWARD, 150, FORWARD), 2.0, 0.025)
        b = drive((150, BACKWARD, 150, BACKWARD), 2.0, 0.025)
        self.assertAlmostEqual(b.x, -f.x, places=9)
        self.assertAlmostEqual(b.y, f.y, places=9)
        self.assertAlmostEqual(b.theta, f.theta, places=9)

    def test_right_turn_mirrors_left_turn(self):
        left = drive((100, BACKWARD, 100, FORWARD), 1.0, 0.025)
        right = drive((100, FORWARD, 100, BACKWARD), 1.0, 0.025)
        self.assertGreater(left.theta, 0.0)
        self.assertAlmostEqual(right.theta, -left.theta, places=9)

    def test_result_barely_depends_on_time_step(self):
        # 2026-11-21: the difference was 5 mm and 0.23 degrees.
        coarse = drive((150, FORWARD, 120, FORWARD), 2.0, 0.025)
        fine = drive((150, FORWARD, 120, FORWARD), 2.0, 0.0025)
        self.assertLess(math.hypot(coarse.x - fine.x, coarse.y - fine.y), 0.01)
        self.assertLess(abs(coarse.theta - fine.theta), math.radians(0.5))


if __name__ == "__main__":
    unittest.main()
