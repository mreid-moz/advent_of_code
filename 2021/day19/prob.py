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
    self.orientation = orientations[0]

  def add_line(self, beacon):
    self.add([int(n) for n in beacon.split(',')])

  def add(self, point):
    self.beacons.append(point)

  def get_beacons(self):
    return [transform(b, self.orientation) for b in self.beacons]

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
      current_scanner = Scanner(line)
      scanners.append(current_scanner)
      continue
    if len(line) == 0:
      continue
    current_scanner.add_line(line)
  return scanners

scanners = parse_scanners(my_input)
logging.debug(f"Found {len(scanners)} scanners.")

def find_pair(some_scanners):
  for i, s1 in enumerate(some_scanners):
    for j, s2 in enumerate(some_scanners[i+1:]):
      #logging.debug(f"Looking for matching pair between {i} and {j}")
      for k, orientation in enumerate(orientations):
        s2.orientation = orientation
        offsets = s1.get_offset(s2)
        if offsets:
          logging.debug(f"{s1.name} and {s2.name} are congruent in orientation {k} with offsets {offsets}")
          return s1, s2, offsets

num_scanners = len(scanners)
relative_matches = {}
while len(relative_matches) < num_scanners:
  logging.debug(f"So far found {len(relative_matches)} relative matches")
  for i, s1 in enumerate(scanners):
    for j, s2 in enumerate(scanners[i+1:]):
      #logging.debug(f"Looking for matching pair between {i} and {j}")
      for k, orientation in enumerate(orientations):
        s2.orientation = orientation
        offsets = s1.get_offset(s2)
        if offsets:
          logging.debug(f"{s1.name} and {s2.name} are congruent in orientation {k} with offsets {offsets}")
          relative_matches[i] = {"match": j, "offsets": offsets, "backwards": False}
          relative_matches[j] = {"match": i, "offsets": offsets, "backwards": True}
          break


for k, v in relative_matches.items():
  if not v['backwards']:
    logging.debug(f"Found a match between {k} and {v['match']}")


reference_scanner = scanners[19]
for scanner in scanners:
  reference_scanner = scanner


  logging.info(f"Part 1: Overall, found {len(scanners[0].beacons)} beacons starting from {scanner.name}")
#for b in sorted(scanners[0].beacons):
#  logging.debug(b)


