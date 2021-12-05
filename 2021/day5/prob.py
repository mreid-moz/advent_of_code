import logging
import copy
import sys
from collections import defaultdict

logging.basicConfig(level=logging.INFO)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [l.strip().split(' -> ') for l in fin.readlines()]
  #coords = [line.strip().split(' -> ')]

floor = defaultdict(int)

for coord in my_input:
  c1, c2 = coord
  x1, y1 = c1.split(',')
  x2, y2 = c2.split(',')
  if x1 != x2 and y1 != y2:
    # diagonal
    pass
  else:
    # horizontal/vertical
    xmin = min(int(x1), int(x2))
    xmax = max(int(x1), int(x2))
    ymin = min(int(y1), int(y2))
    ymax = max(int(y1), int(y2))

    for x in range(xmin, xmax+1):
      for y in range(ymin, ymax+1):
        point = '{},{}'.format(x, y)
        floor[point] += 1

dangers = 0
for k, v in floor.items():
  if v >= 2:
    logging.debug("found a danger zone at {} where {} lines overlap".format(k, v))
    dangers += 1

logging.info("Part 1: Found {} dangerous points".format(dangers))

floor = defaultdict(int)

for coord in my_input:
  c1, c2 = coord
  x1, y1 = [int(t) for t in c1.split(',')]
  x2, y2 = [int(t) for t in c2.split(',')]
  xmin = min(x1, x2)
  xmax = max(x1, x2)
  ymin = min(y1, y2)
  ymax = max(y1, y2)
  xdiff = xmax - xmin
  ydiff = ymax - ymin

  if x1 != x2 and y1 != y2:
    # diagonal
    if x1 < x2:
      if y1 < y2:
        # 0,0 -> 8,8
        #   p1 . .
        #    . \ .
        #    . . p2
        for d in range(xdiff+1):
          x = xmin + d
          y = ymin + d
          point = '{},{}'.format(x, y)
          logging.debug("diagonal type 1 from {},{} to {},{} contains {}".format(x1, y1, x2, y2, point))
          floor[point] += 1
      else:
        # 5,5 to 8,2
        #    . . p2
        #    . / .
        #   p1 . .
        for d in range(xdiff+1):
          x = xmin + d
          y = ymax - d
          point = '{},{}'.format(x, y)
          logging.debug("diagonal type 2 from {},{} to {},{} contains {}".format(x1, y1, x2, y2, point))
          floor[point] += 1
    else: # x1 > x2
      if y1 < y2:
        # 8,0 -> 0,8
        #    . . p1
        #    . / .
        #   p2 . .
        for d in range(xdiff+1):
          x = xmin + d
          y = ymax - d
          point = '{},{}'.format(x, y)
          logging.debug("diagonal type 3 from {},{} to {},{} contains {}".format(x1, y1, x2, y2, point))
          floor[point] += 1
      else:
        # 6,4 -> 2,0
        #   p2 . .
        #    . \ .
        #    . . p1
        for d in range(xdiff+1):
          x = xmin + d
          y = ymin + d
          point = '{},{}'.format(x, y)
          logging.debug("diagonal type 4 from {},{} to {},{} contains {}".format(x1, y1, x2, y2, point))
          floor[point] += 1

  else:
    # horizontal/vertical
    for x in range(xmin, xmax+1):
      for y in range(ymin, ymax+1):
        point = '{},{}'.format(x, y)
        floor[point] += 1

dangers = 0
for k, v in floor.items():
  if v >= 2:
    logging.debug("found a danger zone at {} where {} lines overlap".format(k, v))
    dangers += 1

logging.info("Part 2: Found {} dangerous points".format(dangers))
