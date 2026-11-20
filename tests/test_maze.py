import unittest

from mazesim import maze as mz


class TestMaze(unittest.TestCase):
    def test_follows_track_rules_over_many_seeds(self):
        for seed in range(300):
            m = mz.generate(6, 4, seed=seed)
            self.assertEqual(mz.check_rules(m), [], f"seed {seed}")

    def test_same_seed_same_maze(self):
        a, b = mz.generate(5, 5, seed=7), mz.generate(5, 5, seed=7)
        self.assertEqual(a.open, b.open)
        self.assertEqual(a.goal, b.goal)

    def test_check_rules_catches_a_loop(self):
        m = mz.generate(4, 4, seed=1)
        # Open one more closed inner side: makes a loop.
        for (c, r), dirs in m.open.items():
            if mz.E not in dirs and c < m.cols - 1:
                dirs.add(mz.E)
                m.open[(c + 1, r)].add(mz.W)
                break
        self.assertTrue(any("not a tree" in p for p in mz.check_rules(m)))

    def test_walls_and_entrance(self):
        m = mz.generate(3, 3, seed=3)
        segs = m.wall_segments()
        self.assertTrue(segs)
        x0 = m.entrance[0] * mz.CELL
        entrance_side = ((x0, 0.0), (x0 + mz.CELL, 0.0))
        self.assertNotIn(entrance_side, segs)       # the way in is open


if __name__ == "__main__":
    unittest.main()
