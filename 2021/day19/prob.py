import logging
import re
import sys
from collections import defaultdict

logging.basicConfig(level=logging.DEBUG)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [l.strip() for l in fin.readlines()]

# https://www.euclideanspace.com/maths/algebra/matrix/transforms/examples/index.htm
orientations = [
 [[ 1,  0,  0,],
  [ 0,  1,  0, ],
  [ 0,  0,  1  ]],

 [[ 1,  0,  0,],
  [ 0,  0, -1, ],
  [ 0,  1,  0  ]],

 [[ 1,  0,  0,],
  [ 0, -1,  0, ],
  [ 0,  0, -1  ]],

 [[ 1,  0,  0,],
  [ 0,  0,  1, ],
  [ 0, -1,  0  ]],

 [[ 0, -1,  0,],
  [ 1,  0,  0, ],
  [ 0,  0,  1  ]],

 [[ 0,  0,  1,],
  [ 1,  0,  0, ],
  [ 0,  1,  0  ]],

 [[ 0,  1,  0,],
  [ 1,  0,  0, ],
  [ 0,  0,  -1  ]],

 [[ 0,  0, -1,],
  [ 1,  0,  0, ],
  [ 0, -1,  0  ]],

 [[-1,  0,  0,],
  [ 0, -1,  0, ],
  [ 0,  0,  1  ]],


 [[-1,  0,  0,],
  [ 0,  0, -1, ],
  [ 0, -1,  0  ]],

 [[-1,  0,  0,],
  [ 0,  1,  0, ],
  [ 0,  0, -1  ]],

 [[-1,  0,  0,],
  [ 0,  0,  1, ],
  [ 0,  1,  0  ]],

 [[ 0,  1,  0,],
  [ 1,  0,  0, ],
  [ 0,  0,  1  ]],

 [[ 0,  0,  1,],
  [ 1,  0,  0, ],
  [ 0, -1,  0  ]],

 [[ 0, -1,  0,],
  [ 1,  0,  0, ],
  [ 0,  0, -1  ]],

 [[ 0,  0, -1,],
  [ 1,  0,  0, ],
  [ 0,  1,  0  ]],

 [[ 0,  0, -1,],
  [ 0,  1,  0, ],
  [ 1,  0,  0  ]],

 [[ 0,  1,  0,],
  [ 0,  0,  1, ],
  [ 1,  0,  0  ]],

 [[ 0,  0,  1,],
  [ 0, -1,  0, ],
  [ 1,  0,  0  ]],

 [[ 0, -1,  0,],
  [ 0,  0, -1, ],
  [ 1,  0,  0  ]],

 [[ 0,  0, -1,],
 [  0, -1,  0, ],
 [ -1,  0,  0  ]],

 [[ 0, -1,  0,],
 [  0,  0,  1, ],
 [ -1,  0,  0  ]],

 [[ 0,  0,  1,],
 [  0,  1,  0, ],
 [ -1,  0,  0  ]],

 [[ 0,  1,  0,],
 [  0,  0, -1, ],
 [ -1,  0,  0  ]],

]

def manhattan(p0, p1=(0,0,0)):
   x0, y0, z0 = p0
   x1, y1, z1 = p1
   return abs(x1 - x0) + abs(y1 - y0) + abs(z1 - z0)

def transform(point, orientation):
  if orientation == orientations[0]:
    return point
  x0, y0, z0 = point

  x1 = x0 * orientation[0][0] + y0 * orientation[0][1] + z0 * orientation[0][2]
  y1 = x0 * orientation[1][0] + y0 * orientation[1][1] + z0 * orientation[1][2]
  z1 = x0 * orientation[2][0] + y0 * orientation[2][1] + z0 * orientation[2][2]

  #logging.debug(f"{x0}, {y0}, {z0} -> {x1}, {y1}, {z1}")
  return [x1, y1, z1]

class Scanner:
  def __init__(self, name):
    self.name = name
    self.beacons = []
    self.orientation_idx = 0

  def add_line(self, beacon):
    self.add([int(n) for n in beacon.split(',')])

  def add(self, point):
    self.beacons.append(point)

  def get_beacons(self):
    return [transform(b, orientations[self.orientation_idx]) for b in self.beacons]

  def get_offset(self, other, threshold=12):
    my_beacons = self.get_beacons()
    their_beacons = other.get_beacons()

    diffs = defaultdict(int)

    # they're not in order
    for my in my_beacons:
      for their in their_beacons:
        offset = (my[0] - their[0], my[1] - their[1], my[2] - their[2])
        diffs[offset] += 1
        if diffs[offset] >= threshold:
          return offset
    return None

def parse_scanners(some_input):
  scanners = []
  current_scanner = None
  for line in some_input:
    if re.search('scanner', line):
      current_scanner = Scanner('s' + line.strip(' -scanner'))
      scanners.append(current_scanner)
      continue
    if len(line) == 0:
      continue
    current_scanner.add_line(line)
  return scanners

def find_match(some_scanners, target):
  for i, s in enumerate(some_scanners):
    if s == target:
      continue
    for k in range(len(orientations)):
      s.orientation_idx = k
      offsets = target.get_offset(s)
      if offsets:
        logging.debug(f"{target.name} and {s.name} are congruent in orientation {k} with offsets {offsets}")
        return s, offsets
  return None, None

def combine_scanners(scanners):
  seeds = [scanners.pop()]
  while True:
    found = False
    target = seeds[-1]
    match, offsets = find_match(scanners, target)
    if match is not None:
      found = True
      scanners.remove(match)
      xo, yo, zo = offsets
      logging.debug(f"Adding up to {len(match.beacons)} beacons from {match.name} to seed {target.name}")

      target_beacons = target.get_beacons()
      for x, y, z in match.get_beacons():
        p = [x + xo, y + yo, z + zo]
        if p not in target_beacons:
          target.add(p)
      logging.info(f"After combining beacons, target had {len(target.beacons)} beacons.")
    if len(scanners) == 0:
      break
    if not found:
      seeds.append(scanners.pop())
  return seeds

def reorient(s1, s2):
  for k1 in range(len(orientations)):
    for k2 in range(len(orientations)):
      s1.orientation_idx = k1
      s2.orientation_idx = k2
      offsets = s1.get_offset(s2)
      if offsets:
        #logging.debug(f"{s1.name} in orientation {k1} is congruent to {s2.name} in orientation {k2} with offsets {offsets}")
        return offsets
  return None

scanners = parse_scanners(my_input)
logging.debug(f"Found {len(scanners)} scanners.")

neighbours = defaultdict(list)
for i, s1 in enumerate(scanners):
  for j, s2 in enumerate(scanners):
    if i == j:
      continue
    offsets = reorient(s1, s2)
    if offsets:
      logging.debug(f"{s1.name} in orientation {s1.orientation_idx} is congruent to {s2.name} in orientation {s2.orientation_idx} with offsets {offsets}")
      neighbours[s1.name].append(s2.name)

for n, c in neighbours.items():
  logging.debug(f"Scanner {n} has {len(c)} neighbours: {c}")



#logging.info("Max distance: {}".format(max(distances)))
