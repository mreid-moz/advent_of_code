import logging
import copy
import re
import sys
from collections import defaultdict
from functools import reduce

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




scanners = []
current_scanner = None
for line in my_input:
  if re.search('scanner', line):
    current_scanner = Scanner(line)
    scanners.append(current_scanner)
    continue
  if len(line) == 0:
    continue
  current_scanner.add_line(line)

logging.debug(f"Found {len(scanners)} scanners.")

relative_scanner = None
done = False
for i, s1 in enumerate(scanners):
  if done:
    break
  for j, s2 in enumerate(scanners[1:]):
    matchy = False
    offsets = None
    for k, orientation in enumerate(orientations):
      s2.orientation = orientation
      offsets = s1.get_offset(s2)
      if offsets:
        logging.debug(f"{s1.name} and {s2.name} are congruent in orientation {k} with offsets ({offsets})")
        matchy = True
        break
    if matchy:
      if relative_scanner is None:
        relative_scanner = s1
      xo, yo, zo = offsets
      logging.debug(f"Adding beacons from {s2.name}")
      for x, y, z in s2.get_beacons():
        p = [x + xo, y + yo, z + zo]
        if p not in relative_scanner.beacons:
          relative_scanner.add(p)
        #else:
        #  logging.debug(f"relative scanner already had a beacon at {p}")
      done = True
    else:
      logging.debug(f"Could not find a matching orientation with anyone for {s1.name}")


remaining_scanners = [s for s in scanners if s != relative_scanner]
while remaining_scanners:
  logging.debug(f"Looking through {len(remaining_scanners)} more scanners.")
  for i, s in enumerate(remaining_scanners):
    matchy = False
    offsets = None
    for k, orientation in enumerate(orientations):
      s.orientation = orientation
      offsets = relative_scanner.get_offset(s)
      if offsets:
        logging.debug(f"{relative_scanner.name} and {s.name} are congruent in orientation {k} with offsets ({offsets})")
        matchy = True
        break
    if matchy:
      done = remaining_scanners.pop(i)
      xo, yo, zo = offsets
      logging.debug(f"Adding beacons from {done.name}")
      for x, y, z in done.get_beacons():
        p = [x + xo, y + yo, z + zo]
        if p not in relative_scanner.beacons:
          relative_scanner.add(p)
        #else:
        #  logging.debug(f"relative scanner already had a beacon at {p}")
    else:
      logging.debug(f"Could not find a matching orientation with {s.name}")

logging.info(f"Part 1: Overall, found {len(relative_scanner.beacons)} beacons")


