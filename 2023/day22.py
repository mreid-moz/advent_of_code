from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2023, day=22)

TEST = False
if TEST:
    lines = p.examples[0].input_data.splitlines()
else:
    lines = p.input_data.splitlines()

names = []
letters = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)]
for i in range(len(letters)):
    for j in range(len(letters)):
        names.append(letters[i] + letters[j])

class Brick:
    def __init__(self, line, name):
        self.name = name
        coords = line.split('~')
        x1, y1, z1 = [int(c) for c in coords[0].split(',')]
        x2, y2, z2 = [int(c) for c in coords[1].split(',')]
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1

        self.x2 = x2
        self.y2 = y2
        self.z2 = z2

        self.p1 = (x1, y1, z1)
        self.p2 = (x2, y2, z2)

    def get_width(self):
        return self.x2 - self.x1 + 1

    def get_depth(self):
        return self.y2 - self.y1 + 1

    def get_height(self):
        return self.z2 - self.z1 + 1

    def contains(self, other_x, other_y, other_z):
        return (other_x >= min(self.x1, self.x2) and
               other_x <= max(self.x1, self.x2) and
               other_y >= min(self.y1, self.y2) and
               other_y <= max(self.y1, self.y2) and
               other_z >= min(self.z1, self.z2) and
               other_z <= max(self.z1, self.z2))

def project(bricks, axis=0):
    lines = []
    other_axis = 1
    if axis != 0:
        other_axis = 0

    min_a = min([min(b.p1[axis], b.p2[axis]) for b in bricks])
    max_a = max([max(b.p1[axis], b.p2[axis]) for b in bricks])

    min_o = min([min(b.p1[other_axis], b.p2[other_axis]) for b in bricks])
    max_o = max([max(b.p1[other_axis], b.p2[other_axis]) for b in bricks])

    min_z = min([min(b.z1, b.z2) for b in bricks])
    max_z = max([max(b.z1, b.z2) for b in bricks])

    lines = []
    for z in range(max_z + 1):
        line = []
        point = [0,0,z]
        for a in range(max_a + 1):
            point[axis] = a
            visible_brick = '.'
            for o in range(max_o + 1):
                found = False
                point[other_axis] = o
                for b in bricks:
                    if b.contains(*point):
                        logging.debug("Brick {} ({}-{}) contained {}".format(b.name, b.p1, b.p2, point))
                        visible_brick = b.name
                        found = True
                        break
                if found:
                    break
            line.append(visible_brick)
        lines.append(''.join(line))
        line = []
    return reversed(lines)





bricks = [Brick(line, names[i]) for i, line in enumerate(lines)]

max_width = max([b.get_width() for b in bricks])
max_depth = max([b.get_depth() for b in bricks])
max_height = max([b.get_height() for b in bricks])

logging.debug("Found maxes: width: {}, depth: {}, height: {}".format(max_width, max_depth, max_height))

# First we gotta drop 'em
bricks.sort(key=lambda b: min(b.z1, b.z2))
for b in bricks:
    logging.debug("Found a brick {} at {}-{}".format(b.name, b.z1, b.z2))

proj_x = project(bricks)
logging.debug("Projected in X view:")
for line in proj_x:
    logging.debug(line)


proj_y = project(bricks, axis=1)
logging.debug("Projected in Y view:")
for line in proj_y:
    logging.debug(line)
