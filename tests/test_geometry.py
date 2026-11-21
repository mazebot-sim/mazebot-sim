import math
import unittest

from mazesim.geometry import point_segment_distance, ray_distance

WALL = ((1.0, -1.0), (1.0, 1.0))     # vertical wall at x = 1


class TestGeometry(unittest.TestCase):
    def test_ray_hits_wall_ahead(self):
        self.assertAlmostEqual(ray_distance((0, 0), 0.0, [WALL]), 1.0)

    def test_ray_at_an_angle(self):
        d = ray_distance((0, 0), math.radians(30), [WALL])
        self.assertAlmostEqual(d, 1 / math.cos(math.radians(30)))

    def test_ray_misses_behind_and_beyond_range(self):
        self.assertIsNone(ray_distance((0, 0), math.pi, [WALL]))
        self.assertIsNone(ray_distance((0, 0), 0.0, [WALL], max_range=0.5))

    def test_nearest_of_two(self):
        near = ((0.5, -1.0), (0.5, 1.0))
        self.assertAlmostEqual(ray_distance((0, 0), 0.0, [WALL, near]), 0.5)

    def test_point_segment_distance(self):
        self.assertAlmostEqual(point_segment_distance((0, 0), WALL), 1.0)
        self.assertAlmostEqual(point_segment_distance((1, 2), WALL), 1.0)


if __name__ == "__main__":
    unittest.main()
