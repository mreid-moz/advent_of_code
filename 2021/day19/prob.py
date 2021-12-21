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
  [ 0,  1,  0,],
  [ 0,  0,  1 ]],

 [[ 1,  0,  0,],
  [ 0,  0, -1,],
  [ 0,  1,  0 ]],

 [[ 1,  0,  0,],
  [ 0, -1,  0,],
  [ 0,  0, -1 ]],

 [[ 1,  0,  0,],
  [ 0,  0,  1,],
  [ 0, -1,  0 ]],

 [[ 0, -1,  0,],
  [ 1,  0,  0,],
  [ 0,  0,  1 ]],

 [[ 0,  0,  1,],
  [ 1,  0,  0,],
  [ 0,  1,  0 ]],

 [[ 0,  1,  0,],
  [ 1,  0,  0,],
  [ 0,  0,  -1 ]],

 [[ 0,  0, -1,],
  [ 1,  0,  0,],
  [ 0, -1,  0 ]],

 [[-1,  0,  0,],
  [ 0, -1,  0,],
  [ 0,  0,  1 ]],

 [[-1,  0,  0,],
  [ 0,  0, -1,],
  [ 0, -1,  0 ]],

 [[-1,  0,  0,],
  [ 0,  1,  0,],
  [ 0,  0, -1 ]],

 [[-1,  0,  0,],
  [ 0,  0,  1,],
  [ 0,  1,  0 ]],

 [[ 0,  1,  0,],
  [-1,  0,  0,],
  [ 0,  0,  1 ]],

 [[ 0,  0,  1,],
  [-1,  0,  0,],
  [ 0, -1,  0 ]],

 [[ 0, -1,  0,],
  [-1,  0,  0,],
  [ 0,  0, -1 ]],

 [[ 0,  0, -1,],
  [-1,  0,  0,],
  [ 0,  1,  0 ]],

 [[ 0,  0, -1,],
  [ 0,  1,  0,],
  [ 1,  0,  0 ]],

 [[ 0,  1,  0,],
  [ 0,  0,  1,],
  [ 1,  0,  0 ]],

 [[ 0,  0,  1,],
  [ 0, -1,  0,],
  [ 1,  0,  0 ]],

 [[ 0, -1,  0,],
  [ 0,  0, -1,],
  [ 1,  0,  0 ]],

 [[ 0,  0, -1,],
  [ 0, -1,  0,],
  [-1,  0,  0 ]],

 [[ 0, -1,  0,],
  [ 0,  0,  1,],
  [-1,  0,  0 ]],

 [[ 0,  0,  1,],
  [ 0,  1,  0,],
  [-1,  0,  0 ]],

 [[ 0,  1,  0,],
  [ 0,  0, -1,],
  [-1,  0,  0 ]],

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

  return [x1, y1, z1]

class Scanner:
  def __init__(self, name):
    self.name = name
    self.beacons = []
    self.orientation_idx = 0
    self.position = None

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

def reorient_one(s1, s2):
  for k in range(len(orientations)):
    s2.orientation_idx = k
    offsets = s1.get_offset(s2)
    if offsets:
      logging.debug(f"{s1.name} in orientation {s1.orientation_idx} is congruent to {s2.name} in orientation {s2.orientation_idx} with offsets {offsets}")
      return offsets

scanners = parse_scanners(my_input)
logging.debug(f"Found {len(scanners)} scanners.")

positions = {"s0": [0,0,0]}
ref_scanner = scanners.pop(0)

while len(scanners) > 0:
  for i, s1 in enumerate(scanners):
    s = scanners[i]
    offsets = reorient_one(ref_scanner, s)
    if offsets is not None:
      scanners.pop(i)
      xo, yo, zo = offsets
      for x, y, z in s.get_beacons():
        b = [x + xo, y + yo, z + zo]
        if b not in ref_scanner.beacons:
          ref_scanner.beacons.append(b)
      if s.name not in positions:
        positions[s.name] = offsets

logging.info(f"Num beacons: {len(ref_scanner.beacons)}")

max_distance = 0
key_list = sorted(list(positions.keys()))
for i, s1 in enumerate(key_list):
  for j, s2 in enumerate(key_list[i+1:]):
    a = positions[s1]
    b = positions[s2]
    m = manhattan(a, b)
    if m > max_distance:
      max_distance = m

logging.info(f"Max distance: {max_distance}")

