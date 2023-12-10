from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.INFO)

p = Puzzle(year=2023, day=10)

TEST = True
if TEST:
    lines = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L""".splitlines()
else:
    lines = p.input_data.splitlines()

# lines[y][x] == coordinate

NORTH = 'North'
SOUTH = 'South'
EAST = 'East'
WEST = 'West'
DONE = 'Done'

max_y = len(lines)
max_x = len(lines[0])

sx = None
sy = None

for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if c == 'S':
            sx = x
            sy = y
            logging.info("Found start at ({},{})".format(sx, sy))
            break

def draw(gross):
    return gross.translate(str.maketrans('FJL7','┌┘└┐'))

def follow_path(x, y, direction):
    logging.debug("Following path from {},{} facing {}".format(x, y, direction))
    current = lines[y][x]
    nxt = None
    if direction == NORTH:
        nx, ny = x, y - 1
        if y < 0:
            return (nx, ny, None)
        nxt = lines[ny][nx]
        if nxt == '|':
            return (nx, ny, NORTH)
        if nxt == 'F':
            return (nx, ny, EAST)
        if nxt == '7':
            return (nx, ny, WEST)
        if nxt == 'S':
            return (nx, ny, DONE)
        return (nx, ny, None)

    if direction == SOUTH:
        nx, ny = x, y + 1
        if y > max_y:
            return (nx, ny, None)
        nxt = lines[ny][nx]
        if nxt == '|':
            return (nx, ny, SOUTH)
        if nxt == 'L':
            return (nx, ny, EAST)
        if nxt == 'J':
            return (nx, ny, WEST)
        if nxt == 'S':
            return (nx, ny, DONE)
        return (nx, ny, None)

    if direction == EAST:
        nx, ny = x + 1, y
        if x > max_x:
            return (nx, ny, None)
        nxt = lines[ny][nx]
        if nxt == '-':
            return (nx, ny, EAST)
        if nxt == '7':
            return (nx, ny, SOUTH)
        if nxt == 'J':
            return (nx, ny, NORTH)
        if nxt == 'S':
            return (nx, ny, DONE)
        return (nx, ny, None)

    if direction == WEST:
        nx, ny = x - 1, y
        if x < 0:
            return (nx, ny, None)
        nxt = lines[ny][nx]
        if nxt == '-':
            return (nx, ny, WEST)
        if nxt == 'F':
            return (nx, ny, SOUTH)
        if nxt == 'L':
            return (nx, ny, NORTH)
        if nxt == 'S':
            return (nx, ny, DONE)
        return (nx, ny, None)

loop = set()
loop.add((sx, sy))
candidates = []
for d in [NORTH, SOUTH, EAST, WEST]:
    nx, ny, nd = follow_path(sx, sy, d)
    if nd is not None:
        logging.debug("We can move {} from {},{} to {},{} (then {}).".format(d, sx, sy, nx, ny, nd))
        candidates.append((nx, ny, nd))

# pick one and follow it until we get back to the start.
cx, cy, cd = candidates[0]
loop.add((cx, cy))
nx, ny, nd = follow_path(cx, cy, cd)
loop.add((nx, ny))
logging.debug("We can move {} from {},{} to {},{} (then {}).".format(cd, cx, cy, nx, ny, nd))

# current_path_length = 2
while nd != DONE:
    nx, ny, nd = follow_path(nx, ny, nd)
    loop.add((nx, ny))
    # logging.debug("Next: {},{} (then {}).".format(nx, ny, nd))
    # current_path_length += 1

logging.info("the total path from S back to S was {}, so furthest was {}".format(len(loop), len(loop) // 2))
if not TEST:
    p.answer_a = len(loop) // 2

# for line in lines:
#     print(draw(line))

# ..F7.      ..┌┐.
# .FJ|.      .┌┘|.
# SJ.L7  ->  S┘.└┐
# |F--J      |┌--┘
# LJ...      └┘...

# ┌┌┐┌S┌┐┌┐┌┐┌┐┌┐┌---┐
# └|└┘||||||||||||┌--┘
# ┌└-┐└┘└┘||||||└┘└-┐┐
# ┌--┘┌--┐||└┘└┘┐┌┐┌┘-
# └---┘┌-┘└┘.||-┌┘└┘┘┐
# |┌|┌-┘┌---┐┌┐-└┐└|┐|
# |┌┌┘┌┐└┐┌-┘┌┐|┘└---┐
# ┐-└-┘└┐||┌┐|└┐┌-┐┌┐|
# └.└┐└┌┘|||||┌┘└┐||└┘
# └┐┘└┘└-┘└┘└┘└--┘└┘.└

# ┌┌┐┌S┌┐┌┐┌┐┌┐┌┐┌---┐
# └|└┘||||||||||||┌--┘
# ┌└-┐└┘└┘||||||└┘└-┐┐
# ┌--┘┌--┐||└┘└┘I┌┐┌┘-
# └---┘┌-┘└┘IIII┌┘└┘┘┐
# |┌|┌-┘┌---┐III└┐└|┐|
# |┌┌┘┌┐└┐┌-┘┌┐II└---┐
# ┐-└-┘└┐||┌┐|└┐┌-┐┌┐|
# └.└┐└┌┘|||||┌┘└┐||└┘
# └┐┘└┘└-┘└┘└┘└--┘└┘.└

# ┌xxxSxxxxxxxxxxxxxxx
# └xxxxxxxxxxxxxxxxxxx
# ┌xxxxxxxxxxxxxxxxxx┐
# xxxxxxxxxxxxxx┐xxx-
# xxxxxxxxxx.||-xxxx┘┐
# |┌|xxxxxxxx┌┐-xx└|┐|
# |┌xxxxxxxxxxx|┘xxxxx
# ┐-xxxxxxxxxxxxxxxxxx
# └.└┐└xxxxxxxxxxxxxxx
# └┐┘└┘xxxxxxxxxxxxx.└

# O┌┐┌S┌┐┌┐┌┐┌┐┌┐┌---┐
# O|└┘||||||||||||┌--┘
# O└-┐└┘└┘||||||└┘└-┐O
# ┌--┘┌--┐||└┘└┘I┌┐┌┘O
# └---┘┌-┘└┘IIII┌┘└┘OO
# OOO┌-┘┌---┐III└┐OOOO
# OO┌┘┌┐└┐┌-┘┌┐II└---┐
# OO└-┘└┐||┌┐|└┐┌-┐┌┐|
# OOOOO┌┘|||||┌┘└┐||└┘
# OOOOO└-┘└┘└┘└--┘└┘OO

# Part 2
points_to_consider = []
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if (x, y) not in loop:
            points_to_consider.append((x, y))

def in_or_out(x, y):
    good_count = 0
    bad_count = 0
    for xi in range(x + 1, max_x - 1, 1):
        nx, ny, nd = follow_path(xi, y, EAST)
        if (xi, y) in loop and nd is not None:
            good_count += 1
        else:
            bad_count += 1
    logging.info("{x},{y}: good count {good_count}, bad count {bad_count}".format(**locals()))

logging.info("Found {} points to consider.".format(len(points_to_consider)))
for xt, yt in points_to_consider:
    in_or_out(xt, yt)

