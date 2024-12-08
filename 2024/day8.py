from aocd.models import Puzzle
from collections import defaultdict
from itertools import permutations
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2024, day=8)

TEST = False
if TEST:
    lines = p.examples[0].input_data.splitlines()
else:
    lines = p.input_data.splitlines()

max_x = len(lines[0])
max_y = len(lines)

def in_bounds(x, y):
    return x >=0 and y >= 0 and x < max_x and y < max_y

m = {}
antennae = defaultdict(list)
# Get distinct antenna types
for x in range(len(lines[0])):
    for y in range(len(lines)):
        c = lines[y][x]
        if c != '.':
            m[(x, y)] = c
            antennae[c].append((x, y))

def find_antinodes(m, antennae, limit_distance=True):
    antinodes = set()
    for antenna, locations in antennae.items():
        if len(locations) <= 1:
            continue
        logging.debug(f"Found {len(locations)} {antenna}'s")
        # Identify all pairs
        for loc_a, loc_b in permutations(locations, 2):
            # Compute anti-nodes
            ax, ay = loc_a
            bx, by = loc_b
            dx = bx - ax
            dy = by - ay

            if not limit_distance:
                antinodes.add(loc_a)
                antinodes.add(loc_b)

            antinode1x = ax - dx
            antinode1y = ay - dy
            # Check if each anti-node is on the map,  if so count it.
            while in_bounds(antinode1x, antinode1y):
                antinodes.add((antinode1x, antinode1y))
                logging.debug(f"Antinode from {loc_a} <> {loc_b}: ({antinode1x},{antinode1y})")
                if limit_distance:
                    break
                antinode1x -= dx
                antinode1y -= dy

            antinode2x = bx + dx
            antinode2y = by + dy
            # Same in the othe direction.
            while in_bounds(antinode2x, antinode2y):
                antinodes.add((antinode2x, antinode2y))
                logging.debug(f"Antinodes from {loc_a} <> {loc_b}: ({antinode2x},{antinode2y})")
                if limit_distance:
                    break
                antinode2x += dx
                antinode2y += dy
    return antinodes

antinodes = find_antinodes(m, antennae)
logging.info(f"Found {len(antinodes)} antinode locations")

if not TEST:
    p.answer_a = len(antinodes)

antinodes = find_antinodes(m, antennae, limit_distance=False)
logging.info(f"Part 2: Found {len(antinodes)} antinode locations")

if not TEST:
    p.answer_b = len(antinodes)
