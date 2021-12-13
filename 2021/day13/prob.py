import logging
import copy
import re
import sys
from collections import defaultdict

logging.basicConfig(level=logging.INFO)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [l.strip() for l in fin.readlines()]

points = set()
folds = []
for line in my_input:
  if re.match('^[0-9]', line):
    i, j = line.split(',')
    points.add((int(i), int(j)))
  elif re.match('^fold', line):
    direction, val = line.split('=')
    folds.append((direction[-1], int(val)))

def mirror(point, axis, distance):
  x, y = point
  if axis == 'x':
    if x > distance:
      x = distance - (x - distance)
  elif axis == 'y':
    if y > distance:
      y = distance - (y - distance)
  return (x, y)

def fold(points, axis, distance):
  new_points = set()
  for p in points:
    new_points.add(mirror(p, axis, distance))
  return new_points

folded = fold(points, folds[0][0], folds[0][1])
logging.info("Found {} points after folding once".format(len(folded)))

for (axis, direction) in folds[1:]:
  folded = fold(folded, axis, direction)

max_x = max([x for x, _ in folded])
max_y = max([y for _, y in folded])
for x in range(max_x + 1):
  for y in range(max_y + 1):
    if (x, y) in folded:
      print('#', end='')
    else:
      print(' ', end='')
  print()