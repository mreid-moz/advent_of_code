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

def total_distance(galaxy_map):
    td = 0
    galaxies = sorted(galaxy_map.keys())
    for i, (x1, y1) in enumerate(galaxies[:-1]):
        for j, (x2, y2) in enumerate(galaxies[i+1:]):
            d = manhattan(x1, y1, x2, y2)
            # logging.debug("Distance from {},{} to {},{} is {}".format(x1, y1, x2, y2, d))
            td += d
    return td

class ExpandableMap:
    def __init__(self, galaxy_map, empty_rows, empty_cols, expansion_factor=1):
        self.galaxy_map = galaxy_map
        self.empty_rows = empty_rows
        self.empty_cols = empty_cols
        self.expansion_factor = expansion_factor
        self.expanded_keys = None

    def expand_key(self, x, y):
        new_x = x + (count_less_than(self.empty_cols, x) * (self.expansion_factor - 1))
        new_y = y + (count_less_than(self.empty_rows, y) * (self.expansion_factor - 1))
        return (new_x, new_y)

    def keys(self):
        if self.expanded_keys is None:
            self.expanded_keys = [self.expand_key(x, y) for (x, y) in self.galaxy_map.keys()]
        return self.expanded_keys

galaxy_map = {}
empty_rows = []
for y, line in enumerate(lines):
    if len(set(line)) == 1: # all dots
        empty_rows.append(y)
        continue
    for x, c in enumerate(line):
        if c == '#':
            galaxy_map[(x, y)] = c

max_y = len(lines)
max_x = len(lines[0]) - 1

logging.debug("Before expanding:")
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

logging.debug("Found empty rows {} and empty cols {} ".format(empty_rows, empty_cols))

# part 1
expanded_galaxy_map = ExpandableMap(galaxy_map, empty_rows, empty_cols, 2)
total_galaxy_distance = total_distance(expanded_galaxy_map)
logging.info("Total distance: {}".format(total_galaxy_distance))
if not TEST:
    p.answer_a = total_galaxy_distance

# part 2
expanded_galaxy_map = ExpandableMap(galaxy_map, empty_rows, empty_cols, 1000000)
total_galaxy_distance = total_distance(expanded_galaxy_map)
logging.info("Total distance: {}".format(total_galaxy_distance))
if not TEST:
    p.answer_b = total_galaxy_distance
