from aocd.models import Puzzle
from collections import defaultdict
from utils import draw_map, neighbours
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)
sys.setrecursionlimit(80000)

p = Puzzle(year=2023, day=18)

TEST = False
if TEST:
    lines = p.examples[0].input_data.splitlines()
else:
    lines = p.input_data.splitlines()

def flood(target_map, perimeter_map, x, y, max_x, max_y, min_x, min_y, level=0):
    # if level % 100 == 0:
    #     logging.debug("Flood recursion level: {}".format(level))

    if level > 8000:
        return
    for nx, ny in neighbours(x, y, min_x, max_x, min_y, max_y):
        if (nx, ny) not in target_map and (nx, ny) not in perimeter_map:
            target_map[(nx, ny)] = '#'
            flood(target_map, perimeter_map, nx, ny, max_x, max_y, min_x, min_y, level + 1)

dig_plan = []
for line in lines:
    direction, distance, colour = line.split(' ')
    distance = int(distance)
    dig_plan.append((direction, distance, colour))

current_position = (0,0)
dig_map = {}
dig_map[current_position] = '#'
min_x, max_x, min_y, max_y = (0,0,0,0)

for (direction, distance, colour) in dig_plan:
    xd, yd = (0, 0)
    if direction == 'D':
        xd, yd = (0, 1)
    elif direction == 'L':
        xd, yd = (-1, 0)
    elif direction == 'R':
        xd, yd = (1, 0)
    else: # 'U'
        xd, yd = (0, -1)
    for i in range(distance):
        cx, cy = current_position
        x2, y2 = (cx + xd, cy + yd)
        # logging.debug("Moving from {},{} to {},{}".format(cx, cy, x2, y2))
        current_position = (x2, y2)
        dig_map[current_position] = '#'
        if x2 > max_x:
            max_x = x2
        if x2 < min_x:
            min_x = x2
        if y2 > max_y:
            max_y = y2
        if y2 < min_y:
            min_y = y2

# dig_map[(0,0)] = '@'
draw_map(dig_map, max_x, max_y, min_x, min_y, default_char=' ')

logging.info("Resulting dig map ranges from x={}..{}, y={}..{}, total perimeter size {}".format(min_x, max_x, min_y, max_y, len(dig_map)))

inside = {}
# empirically found a spot inside.
inside_x = 2
inside_y = 1
if not TEST:
    inside_x, inside_y = (7,0)

# artifically help out the flood fill so the code doesn't blow up when doing recursion...
flood(inside, dig_map, inside_x, inside_y, max_x, max_y, min_x, min_y)
flood(inside, dig_map, 75, -120, max_x, max_y, min_x, min_y)
flood(inside, dig_map, 63, -180, max_x, max_y, min_x, min_y)
flood(inside, dig_map, 177, -70, max_x, max_y, min_x, min_y)
flood(inside, dig_map, 320, -88, max_x, max_y, min_x, min_y)


combined = {}
for k in dig_map.keys():
    combined[k] = '~'
for k in inside.keys():
    combined[k] = '.'
draw_map(combined, max_x, max_y, min_x, min_y, default_char=' ')

perimeter_size = len(dig_map)
inside_size = len(inside)
logging.info("After filling the pool, size was {}+{}={}".format(perimeter_size, inside_size, perimeter_size + inside_size))

if not TEST:
    p.answer_a = perimeter_size + inside_size
