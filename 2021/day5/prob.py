import logging
import copy
import sys
from collections import defaultdict

logging.basicConfig(level=logging.DEBUG)

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
    if x1 == y1 and x2 == y2:
      # easy diagonal
      for x in range(xmin, xmax+1):
        for y in range(xmin, xmax+1):
          point = '{},{}'.format(x, y)
          floor[point] += 1
    else:
      # other diagonal
      # e.g. 9,7 -> 7,9 ==> 9,7 8,8 7,9
      # e.g. 4,6 -> 6,4 ==> 4,6 5,5 6,4
      xdiff = xmax - xmin # 2
      for d in range(xdiff+1):
        x = xmin + d
        y = xmax - d
        point = '{},{}'.format(x, y)
        logging.debug("diagonal from {},{} to {},{} contains {}".format(x1, y1, x2, y2, point))
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
