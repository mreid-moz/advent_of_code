from aocd.models import Puzzle
from collections import defaultdict
from utils import draw_map, neighbours
import logging
import re
import sys
import math

logging.basicConfig(level=logging.DEBUG)
sys.setrecursionlimit(80000)

p = Puzzle(year=2023, day=18)

TEST = True
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
# draw_map(dig_map, max_x, max_y, min_x, min_y, default_char=' ')

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
# draw_map(combined, max_x, max_y, min_x, min_y, default_char=' ')

perimeter_size = len(dig_map)
inside_size = len(inside)
logging.info("After filling the pool, size was {}+{}={}".format(perimeter_size, inside_size, perimeter_size + inside_size))

if not TEST:
    p.answer_a = perimeter_size + inside_size


def shoelace(vertices):
    num_vertices = len(vertices)
    term1 = 0
    term2 = 0
    for i in range(num_vertices):
        xi = vertices[i][0]
        # last x gets paired with first y
        if i < num_vertices - 1:
            yi = vertices[i+1][1]
        else:
            yi = vertices[0][1]
        term1 += xi*yi

        yi = vertices[i][1]
        xi = vertices[0][0]
        # last y gets paired with first x
        if i < num_vertices - 1:
            xi = vertices[i+1][0]
        term2 += xi*yi

    area = abs(term2 - term1) // 2
    return area


# Part 2
coords = [(0,0)]
perimeter = 0
for (_, _, colour) in dig_plan:
    distance = int('0x'+colour[2:7], 0)
    perimeter += distance
    direction = ''
    xd, yd = (0, 0)
    if colour[-2] == '0': # R
        direction = 'R'
        xd, yd = (1, 0)
    elif colour[-2] == '1': # D
        direction = 'D'
        xd, yd = (0, 1)
    elif colour[-2] == '2': # L
        direction = 'L'
        xd, yd = (-1, 0)
    elif colour[-2] == '3': # U
        direction = 'U'
        xd, yd = (0, -1)

    prev_x, prev_y = coords[-1]
    next_x = prev_x + (xd * distance)
    next_y = prev_y + (yd * distance)
    coords.append((next_x, next_y))

    logging.debug("Colour: {} => {} {}. Next coordinate: {},{}".format(colour, direction, distance, next_x, next_y))

area = shoelace(coords)
logging.info("Area: {} (with perimeter: {})".format(area, area + perimeter))

coords.reverse()
area = shoelace(coords)
logging.info("Area: {}".format(area))

# if not TEST:
#     p.answer_b = area

# 201397960113622
#    952408144115
#    952404941483
#    952411346745


def PolygonArea(corners):
    n = len(corners) # of corners
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += corners[i][0] * corners[j][1]
        area -= corners[j][0] * corners[i][1]
    area = abs(area) / 2.0
    return area

logging.info("{} vs {}".format(PolygonArea(coords), shoelace(coords)))
