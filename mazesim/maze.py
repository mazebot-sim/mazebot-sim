"""Random mazes that follow the competition's track rules (ver 0.1):

- corridors one cell (40 cm) wide, only 90 degree turns, no rooms [2.9, 2.10]
- no loops [2.8]: the open passages form a spanning tree of the cells
- at most one four-way crossing [2.11]
- dead ends allowed [2.12]; the goal sits at the end of one [3.3]
- one entrance, which is also the exit [2.7]

Cells are (col, row), with row 0 at the bottom. Directions are N, E, S, W.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field

CELL = 0.40  # metres, corridor width [2.9]

N, E, S, W = "N", "E", "S", "W"
STEP = {N: (0, 1), E: (1, 0), S: (0, -1), W: (-1, 0)}
OPPOSITE = {N: S, S: N, E: W, W: E}


@dataclass
class Maze:
    cols: int
    rows: int
    open: dict = field(default_factory=dict)   # cell -> set of open directions
    entrance: tuple = (0, 0)                     # cell at the edge
    entrance_dir: str = S                        # side of that cell open to the outside
    goal: tuple = (0, 0)                         # a dead end

    def neighbours(self, cell):
        c, r = cell
        for d, (dc, dr) in STEP.items():
            n = (c + dc, r + dr)
            if 0 <= n[0] < self.cols and 0 <= n[1] < self.rows:
                yield d, n

    def degree(self, cell) -> int:
        """Open sides inside the maze (the entrance's outside side not counted)."""
        return len(self.open[cell] - ({self.entrance_dir} if cell == self.entrance else set()))

    def wall_segments(self):
        """Walls as ((x1, y1), (x2, y2)) in metres: every closed cell side, once."""
        segs = []
        for (c, r), dirs in self.open.items():
            x0, y0, x1, y1 = c * CELL, r * CELL, (c + 1) * CELL, (r + 1) * CELL
            sides = {N: ((x0, y1), (x1, y1)), E: ((x1, y0), (x1, y1)),
                     S: ((x0, y0), (x1, y0)), W: ((x0, y0), (x0, y1))}
            for d, seg in sides.items():
                if d in dirs:
                    continue
                # Shared sides once: only S and W of each cell, plus the outer N and E.
                if d == N and r < self.rows - 1:
                    continue
                if d == E and c < self.cols - 1:
                    continue
                segs.append(seg)
        return segs


def generate(cols: int, rows: int, seed: int | None = None) -> Maze:
    """A random maze over all cells: randomised depth-first search from the
    entrance, refusing a fourth passage into a cell once one four-way crossing
    exists. The goal is the dead end farthest from the entrance."""
    rng = random.Random(seed)
    maze = Maze(cols, rows, open={(c, r): set() for c in range(cols) for r in range(rows)})
    maze.entrance = (rng.randrange(cols), 0)
    maze.entrance_dir = S
    maze.open[maze.entrance].add(S)

    four_way = 0
    visited = {maze.entrance}
    stack = [maze.entrance]
    while stack:
        cell = stack[-1]
        options = [(d, n) for d, n in maze.neighbours(cell) if n not in visited]
        rng.shuffle(options)
        moved = False
        for d, n in options:
            if len(maze.open[cell]) == 3 and four_way >= 1:
                break   # this cell would become a second four-way crossing
            if len(maze.open[cell]) == 3:
                four_way += 1
            maze.open[cell].add(d)
            maze.open[n].add(OPPOSITE[d])
            visited.add(n)
            stack.append(n)
            moved = True
            break
        if not moved:
            stack.pop()

    # Cells the search could not reach (walled in by the four-way limit) are
    # joined to any visited neighbour with room, so the maze covers every cell.
    for cell in list(maze.open):
        if cell in visited:
            continue
        for d, n in maze.neighbours(cell):
            if n in visited and len(maze.open[n]) < 3:
                maze.open[cell].add(d)
                maze.open[n].add(OPPOSITE[d])
                visited.add(cell)
                break

    dist = distances(maze, maze.entrance)
    dead_ends = [c for c in dist if maze.degree(c) == 1 and c != maze.entrance]
    maze.goal = max(dead_ends, key=lambda c: dist[c]) if dead_ends else maze.entrance
    return maze


def distances(maze: Maze, start) -> dict:
    """Corridor distance in cells from start to every reachable cell."""
    dist = {start: 0}
    queue = [start]
    while queue:
        cell = queue.pop(0)
        for d in maze.open[cell]:
            if cell == maze.entrance and d == maze.entrance_dir:
                continue
            n = (cell[0] + STEP[d][0], cell[1] + STEP[d][1])
            if n not in dist:
                dist[n] = dist[cell] + 1
                queue.append(n)
    return dist


def check_rules(maze: Maze) -> list:
    """Track-rule violations, empty if the maze is valid."""
    problems = []
    cells = maze.cols * maze.rows
    passages = sum(maze.degree(c) for c in maze.open) // 2
    reach = distances(maze, maze.entrance)
    if len(reach) != cells:
        problems.append(f"only {len(reach)} of {cells} cells reachable")
    if passages != cells - 1:
        problems.append(f"{passages} passages for {cells} cells: not a tree (a loop or a gap)")
    four_ways = sum(1 for c in maze.open if maze.degree(c) == 4)
    if four_ways > 1:
        problems.append(f"{four_ways} four-way crossings, at most 1 allowed")
    if maze.goal == maze.entrance or maze.degree(maze.goal) != 1:
        problems.append("the goal is not at the end of a dead end")
    for (c, r), dirs in maze.open.items():
        for d in dirs:
            if (c, r) == maze.entrance and d == maze.entrance_dir:
                continue
            n = (c + STEP[d][0], r + STEP[d][1])
            if n not in maze.open or OPPOSITE[d] not in maze.open[n]:
                problems.append(f"passage {(c, r)} {d} is one-sided or leaves the maze")
    return problems
