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
    self.position = (0,0,0)

  def add_line(self, beacon):
    self.add([int(n) for n in beacon.split(',')])

  def add(self, point):
    self.beacons.append(point)

  def get_beacons(self):
    return [transform(b, orientations[self.orientation_idx]) for b in self.beacons]

  def get_position(self):
    return self.position
    return transform(self.position, orientations[self.orientation_idx])

  def get_relative_position(self, p):
    x, y, z = self.get_position()
    px, py, pz = p
    return (px - x, py - y, pz - z)

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

def reorient_both(s1, s2):
  for k1 in range(len(orientations)):
    s1.orientation_idx = k1
    offsets = reorient_one(s1, s2)
    if offsets:
      #logging.debug(f"{s1.name} in orientation {k1} is congruent to {s2.name} in orientation {k2} with offsets {offsets}")
      return offsets
  return None

scanners = parse_scanners(my_input)
logging.debug(f"Found {len(scanners)} scanners.")

#neighbours = defaultdict(list)
#for i, s1 in enumerate(scanners):
#  for j, s2 in enumerate(scanners):
#    if i == j:
#      continue
#    offsets = reorient_both(s1, s2)
#    if offsets:
#      logging.debug(f"{s1.name} in orientation {s1.orientation_idx} is congruent to {s2.name} in orientation {s2.orientation_idx} with offsets {offsets}")
#      neighbours[s1.name].append(s2.name)
#
#for n, c in neighbours.items():
#  logging.debug(f"Scanner {n} has {len(c)} neighbours: {c}")

# Scanner s0 has 1 neighbours: ['s24']
# Scanner s1 has 4 neighbours: ['s6', 's10', 's19', 's23']
# Scanner s2 has 3 neighbours: ['s15', 's18', 's21']
# Scanner s3 has 2 neighbours: ['s12', 's13']
# Scanner s4 has 1 neighbours: ['s21']
# Scanner s5 has 1 neighbours: ['s16']
# Scanner s6 has 2 neighbours: ['s1', 's11']
# Scanner s7 has 2 neighbours: ['s11', 's20']
# Scanner s8 has 1 neighbours: ['s12']
# Scanner s9 has 2 neighbours: ['s12', 's22']
# Scanner s10 has 2 neighbours: ['s1', 's17']
# Scanner s11 has 4 neighbours: ['s6', 's7', 's21', 's23']
# Scanner s12 has 5 neighbours: ['s3', 's8', 's9', 's14', 's15']
# Scanner s13 has 3 neighbours: ['s3', 's15', 's18']
# Scanner s14 has 3 neighbours: ['s12', 's17', 's22']
# Scanner s15 has 4 neighbours: ['s2', 's12', 's13', 's17']
# Scanner s16 has 2 neighbours: ['s5', 's24']
# Scanner s17 has 5 neighbours: ['s10', 's14', 's15', 's21', 's23']
# Scanner s18 has 3 neighbours: ['s2', 's13', 's24']
# Scanner s19 has 1 neighbours: ['s1']
# Scanner s20 has 1 neighbours: ['s7']
# Scanner s21 has 4 neighbours: ['s2', 's4', 's11', 's17']
# Scanner s22 has 2 neighbours: ['s9', 's14']
# Scanner s23 has 3 neighbours: ['s1', 's11', 's17']
# Scanner s24 has 3 neighbours: ['s0', 's16', 's18']

# herp derp..

#path = [0, 24, 16, 18, 5, 2, 13, 15, 21, 3, 8, 9, 14, 12, 17, 4, 11, 22, 10, 23, 6, 7, 1, 20, 19]
path = [0,
         24,
          16,
           5,
          18,
           2,
            15,
             12,
              3,
              8,
              9,
               22,
              14,
             17,
              10,
               1,
                6,
                19,
              23,
            21,
             4,
             11,
              6,
              7,
           13,
]

if input_file == 't1':
  path = [0,1,4,2,3]

positions = {"s0": (0,0,0)}

last_scanner = scanners[0]
for p in path[1:]:
  next_scanner = scanners[p]
  offsets = reorient_one(last_scanner, next_scanner)
  if offsets is None:
    logging.warning(f"Not able to combine {last_scanner.name} and {next_scanner.name}")
    #break
  else:
    relative_offsets = last_scanner.get_relative_position(offsets)
    next_scanner.position = relative_offsets
    logging.debug(f"relative offsets: {relative_offsets}, scanner_position = {next_scanner.get_position()}")
    logging.debug(f"Able to combine {last_scanner.name} and {next_scanner.name}. Offsets {offsets} relative to {last_scanner.get_position()} -> {relative_offsets}")

    positions[next_scanner.name] = relative_offsets
  next_scanner.orientation_idx = 0
  last_scanner = next_scanner
  #last_scanner_pos = offsets

max_distance = 0
position_list = list(positions.values())
for i, a in enumerate(position_list):
  for j, b in enumerate(position_list[i+1:]):
    m = manhattan(a, b)
    logging.debug(f"{a} to {b} is {m}")
    if m > max_distance:
      max_distance = m

logging.info(f"Max distance: {max_distance}")

