from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2023, day=24)

TEST = False
if TEST:
    lines = p.examples[0].input_data.splitlines()
else:
    lines = p.input_data.splitlines()


def get_abc(pos, vel):
    x1,y1,_ = pos
    vx,vy,_ = vel
    x2 = x1 + vx
    y2 = y1 + vy
    a = y2 - y1
    b = x1 - x2
    c = (a * x1) + (b * y1)
    return a, b, c


def get_intersection(position1, velocity1, position2, velocity2):
    a1, b1, c1 = get_abc(position1, velocity1)
    a2, b2, c2 = get_abc(position2, velocity2)

    det = (a1 * b2) - (a2 * b1)
    if det == 0:
        return (None, None)

    x = (b2 * c1 - b1 * c2) / det
    y = (a1 * c2 - a2 * c1) / det
    return (x, y)

def in_future(pos, vel, x, y):
    x0, y0, _ = pos
    xd, yd, _ = vel

    xtime = (x - x0) / xd
    logging.debug("realtive to {} {}, {},{} is {}".format(pos, vel, x, y, xtime))
    return xtime > 0

min_bound = 200000000000000
max_bound = 400000000000000
if TEST:
    min_bound = 7
    max_bound = 27

hailstones = []
for line in lines:
    pos, vel = line.split(' @ ')
    px, py, pz = [int(x) for x in pos.split(', ')]
    vx, vy, vz = [int(x) for x in vel.split(', ')]
    hailstones.append(((px, py, pz),(vx, vy, vz)))

num_inside = 0
for i, (p1, v1) in enumerate(hailstones[:-1]):
    for j, (p2, v2) in enumerate(hailstones[i+1:]):
        x, y = get_intersection(p1, v1, p2, v2)
        if x is None:
            logging.debug("No Intersection of {} {} and {} {}!".format(p1, v1, p2, v2))
        else:
            logging.debug("Intersection of {} {} and {} {} was at {},{}".format(p1, v1, p2, v2, x, y))
            if x >= min_bound and x <= max_bound and y >= min_bound and y <= max_bound:
                logging.debug("It was inside bounds")
                p1f = in_future(p1, v1, x, y)
                if p1f:
                    logging.debug("p1 crossed in the future")
                p2f = in_future(p2, v2, x, y)
                if p2f:
                    logging.debug("p2 crossed in the future")

                if p1f and p2f:
                    num_inside += 1
            else:
                logging.debug("It was out of bounds")

logging.info("Number of intersections inside bounds: {}".format(num_inside))
if not TEST:
    p.answer_a = num_inside
