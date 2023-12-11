from aocd.models import Puzzle
from collections import defaultdict
from utils import manhattan
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2023, day=11)

TEST = False
if TEST:
    lines = p.examples[0].input_data.splitlines()
else:
    lines = p.input_data.splitlines()

def draw_map(m, mx, my, print_now=True, default_char='.'):
    lines = []
    for y in range(my+1):
        chars = []
        for x in range(mx+1):
            chars.append(m.get((x, y), default_char))
        lines.append(''.join(chars))
        if print_now:
            print(lines[-1])
    return lines

def count_less_than(nums, target):
    c = 0
    for n in nums:
        if n < target:
            c += 1
    return c

galaxy_map = {}
y_offset = 0
for y, line in enumerate(lines):
    if len(set(line)) == 1: # all dots
        y_offset += 1
        continue
    for x, c in enumerate(line):
        if c == '#':
            galaxy_map[(x, y + y_offset)] = c

max_y = len(lines) + y_offset - 1
max_x = len(lines[0]) - 1

logging.debug("Before expanding columns:")
draw_map(galaxy_map, max_x, max_y)

empty_cols = []
for x in range(max_x + 1):
    is_empty = True
    for y in range(max_y + 1):
        if (x, y) in galaxy_map:
            is_empty = False
            break
    if is_empty:
        empty_cols.append(x)

logging.debug("Found emopty cols {} ".format(empty_cols))

expanded_galaxy_map = {}
for (x, y), v in galaxy_map.items():
    x_offset = count_less_than(empty_cols, x)
    expanded_galaxy_map[(x + x_offset, y)] = v
max_x += len(empty_cols)

logging.debug("After expanding columns:")
draw_map(expanded_galaxy_map, max_x, max_y)

total_distance = 0
galaxies = sorted(expanded_galaxy_map.keys())
for i, (x1, y1) in enumerate(galaxies[:-1]):
    for j, (x2, y2) in enumerate(galaxies[i+1:]):
        d = manhattan(x1, y1, x2, y2)
        logging.debug("Distance from {},{} to {},{} is {}".format(x1, y1, x2, y2, d))
        total_distance += d

logging.info("Total distance: {}".format(total_distance))
if not TEST:
    p.answer_a = total_distance
