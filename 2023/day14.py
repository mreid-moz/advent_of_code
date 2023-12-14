from aocd.models import Puzzle
from collections import defaultdict
from utils import draw_map
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2023, day=14)

TEST = False
if TEST:
    lines = p.examples[0].input_data.splitlines()
else:
    lines = p.input_data.splitlines()

rock_map = {}
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if c != '.':
            rock_map[(x, y)] = c

max_x = len(lines[0])
max_y = len(lines)

NORTH = (0, -1)
SOUTH = (0, 1)
EAST = (1, 0)
WEST = (-1, 0)

def tilt(m, mx, my):
    t = tilt_north(m, mx, my)
    t = tilt_west(t, mx, my)
    t = tilt_south(t, mx, my)
    return tilt_east(t, mx, my)

def tilt_north(m, mx, my):
    rolled = {}
    for x in range(mx):
        if (x, 0) in m:
            rolled[(x, 0)] = m[(x, 0)]

    for y in range(1, my):
        for x in range(mx):
            if (x, y) in m:
                if (m[(x, y)] == '#'):
                    rolled[(x, y)] = m[(x, y)]
                    continue
                # logging.debug("Rolling north from {},{}".format(x, y))
                ry = y
                for yn in range(y, 0, -1):
                    if (x, yn - 1) not in rolled:
                        ry = yn - 1
                    else:
                        break
                if ry < 0:
                    ry = 0
                if (x, ry) not in rolled:
                    # logging.debug("Rolled north from {},{} to {},{}".format(x, y, x, ry))
                    rolled[(x, ry)] = m[(x, y)]
    return rolled


def tilt_south(m, mx, my):
    rolled = {}
    for x in range(mx):
        if (x, my-1) in m:
            rolled[(x, my-1)] = m[(x, my-1)]

    for y in range(my-2, -1, -1):
        for x in range(mx):
            # logging.debug("Looking south fom {},{}".format(x, y))
            if (x, y) in m:
                if (m[(x, y)] == '#'):
                    rolled[(x, y)] = m[(x, y)]
                    continue
                # logging.debug("Rolling south from {},{}".format(x, y))
                ry = y
                for yn in range(y, my - 1, 1):
                    if (x, yn + 1) not in rolled:
                        ry = yn + 1
                    else:
                        break
                if ry >= my-1:
                    ry = my-1
                if (x, ry) not in rolled:
                    # logging.debug("Rolled south from {},{} to {},{}".format(x, y, x, ry))
                    rolled[(x, ry)] = m[(x, y)]
    return rolled

def tilt_west(m, mx, my):
    rolled = {}
    for y in range(my):
        if (0, y) in m:
            rolled[(0, y)] = m[(0, y)]

    for x in range(1, mx):
        for y in range(my):
            # logging.debug("Looking west fom {},{}".format(x, y))
            if (x, y) in m:
                # logging.debug("{},{} was there".format(x, y))
                if (m[(x, y)] == '#'):
                    rolled[(x, y)] = m[(x, y)]
                    continue
                # logging.debug("Rolling west from {},{}".format(x, y))
                rx = x
                for xn in range(x, 0, -1):
                    if (xn - 1, y) not in rolled:
                        rx = xn - 1
                    else:
                        break
                if rx < 0:
                    rx = 0
                if (rx, y) not in rolled:
                    # logging.debug("Rolled west from {},{} to {},{}".format(x, y, rx, y))
                    rolled[(rx, y)] = m[(x, y)]
            # else:
            #     logging.debug("{},{} was not there".format(x, y))
    return rolled

def tilt_east(m, mx, my):
    rolled = {}
    for y in range(my):
        if (mx-1, y) in m:
            rolled[(mx-1, y)] = m[(mx-1, y)]

    for x in range(mx - 2, -1, -1):
        for y in range(my):
            # logging.debug("Looking east fom {},{}".format(x, y))
            if (x, y) in m:
                if (m[(x, y)] == '#'):
                    rolled[(x, y)] = m[(x, y)]
                    continue
                # logging.debug("Rolling east from {},{}".format(x, y))
                rx = x
                for xn in range(x, mx - 1, 1):
                    if (xn + 1, y) not in rolled:
                        rx = xn + 1
                    else:
                        break
                if rx >= mx-1:
                    rx = mx-1
                if (rx, y) not in rolled:
                    # logging.debug("Rolled east from {},{} to {},{}".format(x, y, rx, y))
                    rolled[(rx, y)] = m[(x, y)]
    return rolled


rolled = {}
for x in range(max_x):
    if (x, 0) in rock_map:
        rolled[(x, 0)] = rock_map[(x, 0)]

for y in range(1, max_y):
    for x in range(max_x):
        if (x, y) in rock_map:
            if (rock_map[(x, y)] == '#'):
                rolled[(x, y)] = rock_map[(x, y)]
                continue
            logging.debug("Rolling from {},{}".format(x, y))
            ry = y
            for yn in range(y, 0, -1):
                if (x, yn - 1) not in rolled:
                    ry = yn - 1
                else:
                    break
            if ry < 0:
                ry = 0
            if (x, ry) not in rolled:

                logging.debug("Rolled from {},{} to {},{}".format(x, y, x, ry))
                rolled[(x, ry)] = rock_map[(x, y)]

draw_map(rock_map, max_x - 1, max_y - 1)
print('vvvvvvv')
draw_map(rolled, max_x - 1, max_y - 1)

def tally(m, max_y):
    logging.debug("Max weight: {}".format(max_y))
    t = 0
    for (x, y), c in m.items():
        if c == 'O':
            t += max_y - y
    return t

total_weight = tally(rolled, max_y)
logging.info("Total weight: {}".format(total_weight))


if not TEST:
    p.answer_a = total_weight


# draw_map(rock_map, max_x - 1, max_y - 1)
# print('^^^^ North ^^^^')
# tilted = tilt_north(rock_map, max_x, max_y)
# draw_map(tilted, max_x - 1, max_y - 1)
# print('<<<< West  <<<<')
# tilted = tilt_west(tilted, max_x, max_y)
# draw_map(tilted, max_x - 1, max_y - 1)
# print('vvvv South vvvv')
# tilted = tilt_south(tilted, max_x, max_y)
# draw_map(tilted, max_x - 1, max_y - 1)
# print('>>>> East  >>>>')
# tilted = tilt_east(tilted, max_x, max_y)
# draw_map(tilted, max_x - 1, max_y - 1)

# print('@@@@ After 2 cycles @@@@')
# tilted = tilt(tilted, max_x, max_y)

# draw_map(tilted, max_x - 1, max_y - 1)

seen = {}

tilted = rock_map
target_iterations = 1000000000
current_iteration = 0
while current_iteration < target_iterations:
    tilted = tilt(tilted, max_x, max_y)
    tilted_s = '\n'.join(draw_map(tilted, max_x - 1, max_y - 1, print_now=False))
    if tilted_s not in seen:
        seen[tilted_s] = current_iteration
    else:
        prev = seen[tilted_s]
        logging.info("Previously saw configuration {} on iteration {}".format(current_iteration, prev))
        delta = current_iteration - prev
        remaining = target_iterations - current_iteration
        fast_forward = remaining // delta * delta
        logging.info("Fast forwarding by {}".format(fast_forward))
        current_iteration += fast_forward
    current_iteration += 1

total_weight = tally(tilted, max_y)
logging.info("Total weight: {}".format(total_weight))
if not TEST:
    p.answer_b = total_weight
