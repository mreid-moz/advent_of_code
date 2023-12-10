from aocd.models import Puzzle
from collections import defaultdict
from utils import neighbours
import logging
import re
import sys

logging.basicConfig(level=logging.INFO)

# :-/
sys.setrecursionlimit(50000)

p = Puzzle(year=2023, day=10)

TEST = False
if TEST:
#     lines = """FF7FSF7F7F7F7F7F---7
# L|LJ||||||||||||F--J
# FL-7LJLJ||||||LJL-77
# F--JF--7||LJLJ7F7FJ-
# L---JF-JLJ.||-FJLJJ7
# |F|F-JF---7F7-L7L|7|
# |FFJF7L7F-JF7|JL---7
# 7-L-JL7||F7|L7F-7F7|
# L.L7LFJ|||||FJL7||LJ
# L7JLJL-JLJLJL--JLJ.L""".splitlines()
    lines = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L--7F-J|.
.|...||..|.
.L---JL--J.
...........""".splitlines()
else:
    lines = p.input_data.splitlines()

# lines[y][x] == coordinate

NORTH = 'North'
SOUTH = 'South'
EAST = 'East'
WEST = 'West'
DONE = 'Done'

max_y = len(lines) - 1
max_x = len(lines[0]) - 1

sx = None
sy = None

for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if c == 'S':
            sx = x
            sy = y
            logging.info("Found start at ({},{})".format(sx, sy))
            break

# The input letters are hard on the ol' noggin. Make it look nice.
def draw(gross):
    return gross.translate(str.maketrans('FJL7','┌┘└┐'))

def follow_path(x, y, direction, loop=False):
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
        if y >= max_y:
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
        if x >= max_x:
            return (nx, ny, None)
        nxt = lines[ny][nx]
        if nxt == '-':
            return (nx, ny, EAST)
        if nxt == '7':
            return (nx, ny, SOUTH)
        if nxt == 'J':
            return (nx, ny, NORTH)
        if nxt == 'S':
            if loop:
                return (nx, ny, EAST)
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
            if loop:
                return (nx, ny, WEST)
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

# O┌┐┌S┌┐┌┐┌┐┌┐┌┐┌---┐
# O|└┘||||||||||||┌--┘
# O└-┐└┘└┘||||||└┘└-┐O
# ┌--┘┌--┐||└┘└┘?┌┐┌┘O
# └---┘┌-┘└┘????┌┘└┘OO
# OOO┌-┘┌---┐???└┐OOOO
# OO┌┘┌┐└┐┌-┘┌┐??└---┐
# OO└-┘└┐||┌┐|└┐┌-┐┌┐|
# OOOOO┌┘|||||┌┘└┐||└┘
# OOOOO└-┘└┘└┘└--┘└┘OO

# Part 2
outsides = set()
points_to_consider = []
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if (x, y) not in loop:
            if x == 0 or y == 0 or x == max_x or y == max_y:
                # points around the edge can't be inside.
                outsides.add((x, y))
            else:
                points_to_consider.append((x, y))

def flood(x, y, target):
    updates = 0
    for nx, ny in neighbours(x, y, 0, max_x, 0, max_y):
        if (nx, ny) not in target and (nx, ny) not in loop:
            target.add((nx, ny))
            flood(nx, ny, target)

# Note: we've already turned.
def get_extra_left(x, y, d, c):
    if d == NORTH:
        if c == 'L': # outside corner
            return (x, y+1)
        #if c == 'J': # inside corner
        # return (None, None)

    elif d == SOUTH:
        if c == '7': # outside corner
            return (x, y-1)
        #if c == 'F': # inside corner
        # return (None, None)

    elif d == EAST:
        if c == 'F': # outside corner
            return (x-1, y)
        #if c == 'L': # inside corner
        # return (None, None)

    elif d == WEST:
        if c == 'J': # outside corner
            return (x+1, y)
        #if c == '7': # inside corner
    return (None, None)

# Note: we've already turned.
def get_extra_right(x, y, d, c):
    if d == NORTH:
        if c == 'J': # outside corner
            return (x, y+1)
    elif d == SOUTH:
        if c == 'F': # outside corner
            return (x, y-1)
    elif d == EAST:
        if c == 'L': # outside corner
            return (x-1, y)
    elif d == WEST:
        if c == '7': # outside corner
            return (x+1, y)
    return (None, None)

for ox, oy in [o for o in outsides]:
    flood(ox, oy, outsides)

# Find a spot on the loop where we have a NORTH or SOUTH and we have
# an Outside adjacent.
cx, cy, cd = candidates[0]
nx, ny, nd = follow_path(cx, cy, cd)
while nd != DONE:
    nx, ny, nd = follow_path(nx, ny, nd)
    if nd == NORTH and (nx-1, ny) in outsides:
        logging.info("Moving North at {nx},{ny} had an outside on the left".format(**locals()))
        break
    if nd == NORTH and (nx+1, ny) in outsides:
        logging.info("Moving North at {nx},{ny} had an outside on the right".format(**locals()))
        break

# Now, follow the entire path and mark any other disconnected bits on
# the same side (left, in my inputt) as "out"; bits on the other side
# (right) as "in".
insides = set()
trace_x, trace_y, trace_dir = (126, 121, NORTH)
nx, ny, nd = follow_path(trace_x, trace_y, trace_dir, loop=True)
while not (nx == trace_x and ny == trace_y):
    # find the point to the left
    left_x, left_y = nx, ny
    if nd == NORTH:
        left_x = nx - 1
    elif nd == SOUTH:
        left_x = nx + 1
    elif nd == EAST:
        left_y = ny - 1
    else:
        left_y = ny + 1
    if left_x >= 0 and left_x <= max_x and left_y >= 0 and left_y <= max_y:
        if (left_x, left_y) not in loop:
            # logging.info("Found a tricksy O at {left_x},{left_y}".format(**locals()))
            outsides.add((left_x, left_y))

    # Left of a corner might have 2 directions to check.
    nc = lines[ny][nx]
    extra_x, extra_y = get_extra_left(nx, ny, nd, nc)
    if extra_x is not None:
        if (extra_x, extra_y) not in loop:
            outsides.add((extra_x, extra_y))

    # The point to the right must be inside
    right_x, right_y = nx, ny
    if nd == NORTH:
        right_x = nx + 1
    elif nd == SOUTH:
        right_x = nx - 1
    elif nd == EAST:
        right_y = ny + 1
    else:
        right_y = ny - 1
    if right_x >= 0 and right_x <= max_x and right_y >= 0 and right_y <= max_y:
        if (right_x, right_y) not in loop:
            # logging.info("Found a tricksy I at {right_x},{right_y}".format(**locals()))
            insides.add((right_x, right_y))

    # Right of a corner might have 2 directions to check.
    nc = lines[ny][nx]
    extra_x, extra_y = get_extra_right(nx, ny, nd, nc)
    if extra_x is not None:
        logging.info("Found a corner {nc} going {nd} from {nx},{ny}, so {extra_x},{extra_y} is in".format(**locals()))
        if (extra_x, extra_y) not in loop:
            insides.add((extra_x, extra_y))

    nx, ny, nd = follow_path(nx, ny, nd, loop=True)


for x, y in [i for i in insides]:
    flood(x, y, insides)

# See if we have any unknowns remaining
unk_count = 0
for y, line in enumerate(lines):
    nice = ''
    for x, c in enumerate(line):
        if (x, y) in outsides:
            nice += 'O'
        elif (x, y) in insides:
            nice += 'I'
        elif (x, y) not in loop:
            nice += '?'
            unk_count += 1
        else:
            nice += draw(c)
    print(nice)

logging.info("Found {} insides, {} unknowns".format(len(insides), unk_count))

if unk_count == 0:
    if not TEST:
        p.answer_b = len(insides)
