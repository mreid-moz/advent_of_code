from aocd.models import Puzzle
from collections import defaultdict
from utils import draw_map
import logging
import re
import sys

logging.basicConfig(level=logging.INFO)

p = Puzzle(year=2024, day=6)

TEST = True
if TEST:
    lines = p.examples[0].input_data.splitlines()
else:
    lines = p.input_data.splitlines()

directions = {
    '^': (0, -1, '>'),
    '>': (1, 0, 'v'),
    'v': (0, 1, '<'),
    '<': (-1, 0, '^'),
}

m = {}
start_x = 0
start_y = 0
start_d = '^'
max_y = len(lines)
max_x = len(lines[0])
for y in range(max_y):
    for x in range(max_x):
        if lines[y][x] == '^':
            start_x = x
            start_y = y
        elif lines[y][x] == '#':
            m[(x, y)] = '#'

current_x = start_x
current_y = start_y
current_d = start_d

m_orig = m.copy()

def in_bounds(x, y):
    return x >= 0 and x < max_x and y >=0 and y < max_y

def move(the_map, cx, cy, cd):
    the_map[(cx, cy)] = 'X'
    # logging.debug(f"<Map> ({cx},{cy}) {cd}")
    # draw_map(m, max_x, max_y)
    # logging.debug("</Map>")
    dx, dy, nd = directions[cd]
    nx = cx + dx
    ny = cy + dy
    if the_map.get((nx, ny)) == '#':
        logging.debug(f"Switching direction from {cd} to {nd}")
        cd = nd
    else:
        cx = nx
        cy = ny
    return cx, cy, cd

while in_bounds(current_x, current_y):
    current_x, current_y, current_d = move(m, current_x, current_y, current_d)

spaces = 0
for k, v in m.items():
    if v == 'X':
        spaces += 1

logging.info(f"Found {spaces} spaces.")
if not TEST:
    p.answer_a = spaces

positions = 0
for y in range(max_y):
    for x in range(max_x):
        m = m_orig.copy()
        if (x, y) in m:
            logging.debug(f"Skipping {x},{y}")
            continue

        current_x = start_x
        current_y = start_y
        current_d = start_d
        m[(x, y)] = '#'

        logging.debug(f"Trying obstruction at {x},{y}")

        path = set()
        while in_bounds(current_x, current_y) and (current_x, current_y, current_d) not in path:
            path.add((current_x, current_y, current_d))
            current_x, current_y, current_d = move(m, current_x, current_y, current_d)

        if in_bounds(current_x, current_y):
            logging.info(f"with obstruction at {x},{y} we have a loop")
            positions += 1

logging.info(f"Found {positions} good spots for an obstruction")
if not TEST:
    p.answer_b = positions
