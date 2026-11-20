"""2D geometry: rays against wall segments, for the IR sensors."""
from __future__ import annotations

import math


def ray_distance(origin, angle, segments, max_range=math.inf):
    """Distance from origin along the ray at `angle` (radians, 0 = +x,
    counter-clockwise) to the nearest segment, or None if none within
    max_range."""
    ox, oy = origin
    dx, dy = math.cos(angle), math.sin(angle)
    best = None
    for (x1, y1), (x2, y2) in segments:
        ex, ey = x2 - x1, y2 - y1
        denom = dx * ey - dy * ex
        if abs(denom) < 1e-12:
            continue            # parallel
        # origin + t*d = p1 + u*e
        t = ((x1 - ox) * ey - (y1 - oy) * ex) / denom
        u = ((x1 - ox) * dy - (y1 - oy) * dx) / denom
        if t >= 0 and 0 <= u <= 1 and t <= max_range and (best is None or t < best):
            best = t
    return best


def point_segment_distance(p, seg):
    """Shortest distance from point p to a segment."""
    (x1, y1), (x2, y2) = seg
    px, py = p
    ex, ey = x2 - x1, y2 - y1
    length2 = ex * ex + ey * ey
    if length2 == 0:
        return math.hypot(px - x1, py - y1)
    u = max(0.0, min(1.0, ((px - x1) * ex + (py - y1) * ey) / length2))
    return math.hypot(px - (x1 + u * ex), py - (y1 + u * ey))
