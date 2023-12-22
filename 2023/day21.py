from aocd.models import Puzzle
from collections import defaultdict
from utils import lines_to_map, get_map_bounds, draw_map, neighbours
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2023, day=21)

TEST = False
if TEST:
    lines = p.examples[0].input_data.splitlines()
else:
    lines = p.input_data.splitlines()

garden_map, min_x, max_x, min_y, max_y = lines_to_map(lines)

sx, sy = None, None
for (x, y), c in garden_map.items():
    if c == 'S':
        sx, sy = (x, y)

del garden_map[(sx, sy)]

def step(m, locations, num_steps):
    if num_steps == 0:
        return locations
    next_locations = set()
    for x, y in locations:
        for nx, ny in neighbours(x, y, min_x, max_x, min_y, max_y, include_diagonals=False):
            if (x, y) == (1, 4):
                logging.debug("Found a neighbour of (1,4) at ({},{}). min_x is {}".format(nx, ny, min_x))
            if (nx, ny) in garden_map:
                # it's a rock
                continue
            next_locations.add((nx, ny))
    return step(m, next_locations, num_steps-1)

num_steps = 64
locs = step(garden_map, [(sx, sy)], num_steps)

logging.info("After {} steps, we could reach {} plots".format(num_steps, len(locs)))

for l in locs:
    garden_map[l] = 'O'
draw_map(garden_map, max_x, max_y)
if not TEST:
    p.answer_a = len(locs)
