from aocd.models import Puzzle
from collections import defaultdict
# from utils import draw_map
import logging
import re
import sys

logging.basicConfig(level=logging.INFO)

p = Puzzle(year=2023, day=16)

TEST = False
if TEST:
    lines = p.examples[0].input_data.splitlines()
else:
    lines = p.input_data.splitlines()

max_x = len(lines[0])
max_y = len(lines)

NORTH = 'North'
SOUTH = 'South'
EAST = 'East'
WEST = 'West'

def draw_map(m, mx, my, print_now=True, default_char='.'):
    lines = []
    for y in range(my+1):
        chars = []
        for x in range(mx+1):
            if (x, y) in m:
                chars.append('#')
            else:
                chars.append(default_char)
            # chars.append(m.get((x, y), default_char))
        lines.append(''.join(chars))
        if print_now:
            print(lines[-1])
    return lines

def get_direction_arrow(d):
    if d == NORTH:
        return '^'
    if d == SOUTH:
        return 'v'
    if d == EAST:
        return '>'
    return '<'

mirror_map = {}
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        mirror_map[(x, y)] = c


def trace(m, p, x, y, direction):
    p[(x, y)].add(direction)
    logging.debug("Tracing {} from {},{}".format(direction, x, y))
    currents = follow_path(m, p, x, y, direction)
    current_energized = len(p)
    zero_count = 0
    while len(currents) > 0:
        nexts = []
        for (x, y, d) in currents:
            p[(x, y)].add(d)

            # logging.debug("About to move {} from {},{}".format(d, x, y))
            n = follow_path(m, p, x, y, d)
            for nx, ny, nd in n:
                if nd in p[(nx, ny)]:
                    logging.info("We've already traced {} {},{}".format(nd, nx, ny))
                else:
                    nexts.append((nx, ny, nd))
            logging.debug("Found {} beams to follow".format(len(n)))
            # nexts += n
        currents = nexts
        num_added = len(p) - current_energized
        logging.info("Energized {} more tiles ({} total). {} Beams".format(num_added, len(p), len(currents)))
        current_energized = len(p)


def follow_path(m, p, x, y, direction):
    logging.debug("Following path from {},{} facing {}".format(x, y, direction))

    # t = m[(x, y)]
    # m[(x, y)] = get_direction_arrow(direction)
    # draw_map(m, max_x-1, max_y-1)
    # print('---')
    # m[(x, y)] = t
    current = m[(x, y)]
    nxt = None
    if direction == NORTH:
        nx, ny = x, y - 1
        if ny < 0:
            return []
        nxt = m[(nx, ny)]
        logging.debug("Next position {},{} is {}".format(nx, ny, nxt))
        if nxt == '.' or nxt == '|':
            return [(nx, ny, NORTH)]

        if nxt == '-':
            return [(nx, ny, EAST), (nx, ny, WEST)]
        if nxt == '/':
            return [(nx, ny, EAST)]
        if nxt == '\\':
            return [(nx, ny, WEST)]
        return []

    if direction == SOUTH:
        nx, ny = x, y + 1
        if ny >= max_y:
            return []
        nxt = m[(nx, ny)]
        logging.debug("Next position {},{} is {}".format(nx, ny, nxt))
        if nxt == '.' or nxt == '|':
            return [(nx, ny, SOUTH)]
        if nxt == '-':
            return [(nx, ny, EAST), (nx, ny, WEST)]
        if nxt == '/':
            return [(nx, ny, WEST)]
        if nxt == '\\':
            return [(nx, ny, EAST)]
        return []

    if direction == EAST:
        nx, ny = x + 1, y
        if nx >= max_x:
            return []
        nxt = m[(nx, ny)]
        logging.debug("Next position {},{} is {}".format(nx, ny, nxt))
        if nxt == '.' or nxt == '-':
            return [(nx, ny, EAST)]
        if nxt == '|':
            return [(nx, ny, SOUTH), (nx, ny, NORTH)]
        if nxt == '/':
            return [(nx, ny, NORTH)]
        if nxt == '\\':
            return [(nx, ny, SOUTH)]
        return []

    if direction == WEST:
        nx, ny = x - 1, y
        if nx < 0:
            return []
        nxt = m[(nx, ny)]
        logging.debug("Next position {},{} is {}".format(nx, ny, nxt))
        if nxt == '.' or nxt == '-':
            return [(nx, ny, WEST)]
        if nxt == '|':
            return [(nx, ny, SOUTH), (nx, ny, NORTH)]
        if nxt == '/':
            return [(nx, ny, SOUTH)]
        if nxt == '\\':
            return [(nx, ny, NORTH)]
        return []

path = defaultdict(set)

trace(mirror_map, path, 0, 0, EAST)
logging.info("After tracing, {} tiles were energized".format(len(path)))
draw_map(path, max_x-1, max_y-1)
if not TEST:
    p.answer_a = len(path)
