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

  def add(self, beacon):
    self.beacons.append([int(n) for n in beacon.split(',')])

  def get_beacons(self):
    return [transform(b, self.orientation) for b in self.beacons]

  def get_offset(self, other, threshold=12):
    my_beacons = self.get_beacons()
    their_beacons = other.get_beacons()

    diffs = defaultdict(int)

    for my, their in zip(my_beacons, their_beacons):
      offset = (my[0] - their[0], my[1] - their[1], my[2] - their[2])
      diffs[offset] += 1
      if diffs[offset] >= threshold:
        return offset
    #common_count = [0,0,0]
    #offsets = [0,0,0]
    #for n in range(3):
    #  my_xs = [b[n] for b in my_beacons]
    #  their_xs = [b[n] for b in their_beacons]
    #  diffs = defaultdict(int)
    #  for my,their in zip(my_xs, their_xs):
    #    #logging.debug(f"Found a {n} diff of {my - their}")
    #    diffs[my - their] += 1
    #  for diff, count in diffs.items():
    #    if count > common_count[n]:
    #      common_count[n] = diff
    #      offsets[n] = diff
    #  common_count[n] = max(diffs.values())
    #if (common_count[0] >= threshold and
    #    common_count[1] >= threshold and
    #    common_count[2] >= threshold):
    #   return offsets
    #else:
    #  logging.debug(f"Common counts: {common_count}")
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
  current_scanner.add(line)

logging.debug(f"Found {len(scanners)} scanners.")

relative_scanner = scanners[0]

for i, s2 in enumerate(scanners):
  #for j, s2 in enumerate(scanners[i+1:]):
  matchy = False
  for k, orientation in enumerate(orientations):
    s2.orientation = orientation
    offsets = relative_scanner.get_offset(s2)
    if offsets:
      logging.debug(f"{relative_scanner.name} and {s2.name} are congruent in orientation {k} with offsets ({offsets})")
      matchy = True
      break
    else:
      logging.debug(f"{relative_scanner.name} and {s2.name} are not congruent in orientation {k}")


#logging.info(f"Part 1: Final list: {root}, magnitude is {root.magnitude()}")

#p = [1,2,3]
#for k, orientation in enumerate(orientations):
#  logging.info(f"{p} to {transform(p, orientation)}")


