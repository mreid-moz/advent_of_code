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
  [-1,  0,  0, ],
  [ 0,  0,  1  ]],

 [[ 0,  0,  1,],
  [-1,  0,  0, ],
  [ 0, -1,  0  ]],

 [[ 0, -1,  0,],
  [-1,  0,  0, ],
  [ 0,  0, -1  ]],

 [[ 0,  0, -1,],
  [-1,  0,  0, ],
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

  return [x1, y1, z1]

def undo_transform(point, orientation):
  # Inverse of
  #  [[ 1,  0,  0,],
  #   [ 0,  0, -1, ],
  #   [ 0,  1,  0  ]],
  # is
  #  [[ 1,  0,  0,],
  #   [ 0,  0,  1, ],
  #   [ 0, -1,  0  ]],
  if orientation == orientations[1]:
    return transform(point, orientations[3])
  else:
    logging.warning("Fail: Attempting to invert something smart!")
    return None


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

  def get_position(self):
    return transform(self.position, orientations[self.orientation_idx])

  def get_beacons(self):
    return [transform(b, orientations[self.orientation_idx]) for b in self.beacons]

  def reorient(self):
    #logging.debug(f"Reorienting {self.name}")
    if self.orientation_idx == 0:
      return
    self.beacons = self.get_beacons()
    self.orientation_idx = 0

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
    #else:
    #  logging.debug(f"No match: {s1.name} o{s1.orientation_idx} doesn't match {s2.name} o{s2.orientation_idx}")

def reorient_both(s1, s2):
  for k1 in range(len(orientations)):
    s1.orientation_idx = k1
    offsets = reorient_one(s1, s2)
    if offsets:
      #logging.debug(f"{s1.name} in orientation {k1} is congruent to {s2.name} in orientation {k2} with offsets {offsets}")
      return offsets
  return None

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
# needed some backtracking :(
path = [0,
         24,
          16,
           5, 16, 24,
          18,
           2,
            15,
             12,
              3,
               13, 15,
                17,
                 10,
                  1,
                   6,
                    11,
                     7,
                      20, 7, 11,
                       21,
                        4, 21, 17,
                         23, 1,
                          19, 1, 10, 17, 15, 13, 3, 12,
                           8, 12,
                            9,
                             22,
                              14,
]


# test input:
# Scanner s0 has 1 neighbours: ['s1']
# Scanner s1 has 3 neighbours: ['s0', 's3', 's4']
# Scanner s2 has 1 neighbours: ['s4']
# Scanner s3 has 1 neighbours: ['s1']
# Scanner s4 has 2 neighbours: ['s1', 's2']

if input_file == 't1':
  path = [0,
           1,
            3, 1,
            4,
           2]

# # Part 1:
#scanners = parse_scanners(my_input)
#logging.debug(f"Found {len(scanners)} scanners.")
# reference_scanner = scanners[path[0]]
# for p in path[1:]:
#   current_scanner = scanners[p]
#   offsets = reorient_both(reference_scanner, current_scanner)
#   if offsets is None:
#     logging.warning(f"Not able to combine {reference_scanner.name} and {current_scanner.name}")
#     #break
#   else:
#     xo, yo, zo = offsets
#     for x,y,z in current_scanner.get_beacons():
#       b = [x + xo, y + yo, z + zo]
#       if b not in reference_scanner.beacons:
#         reference_scanner.beacons.append(b)
#
# logging.info(f"Part 1: Found {len(reference_scanner.beacons)} beacons.")

scanners = parse_scanners(my_input)
logging.debug(f"Resetting {len(scanners)} scanners.")

positions = {"s0": (0,0,0)}
last_scanner = scanners[0]
last_scanner.position = [0,0,0]

for p in path[1:]:
  next_scanner = scanners[p]
  prev_orientation = last_scanner.orientation_idx
  offsets = reorient_one(last_scanner, next_scanner)
  if offsets is None:
    logging.warning(f"Not able to combine {last_scanner.name} and {next_scanner.name}")
    #break
  else:
    next_scanner.reorient()
    #x0,y0,z0 = last_scanner.get_position()
    x0,y0,z0 = last_scanner.position
    x1,y1,z1 = offsets
    relative_pos = (x1 + x0, y1 + y0, z1 + z0)
    if last_scanner.orientation_idx != prev_orientation:
      #logging.debug(f"Last scanner orientation changed from {prev_orientation} to {last_scanner.orientation_idx}")
      #logging.debug(f"It's position changed from {last_scanner.position} to {last_scanner.get_position()}")
      if last_scanner.orientation_idx == 1:
        #undone = undo_transform(last_scanner.get_position(), orientations[1])
        relative_pos = undo_transform(relative_pos, orientations[1])
        #logging.debug(f"Undoing set it back to {undone}")
      else:
        logging.warning("don't know how to undo this orientation change.")
    if next_scanner.position is None:
      next_scanner.position = relative_pos
    logging.debug(f"Scanner {last_scanner.name:<3} was at {last_scanner.position}, offsets to {next_scanner.name:<3} were {offsets}, relative position of {next_scanner.name}: {relative_pos}")

    if next_scanner.name not in positions:
      positions[next_scanner.name] = relative_pos
    #else:
    #  logging.info(f"Skipping, not the first time we've seen {next_scanner.name}")
  last_scanner = next_scanner

max_distance = 0
key_list = sorted(list(positions.keys()))
for i, s1 in enumerate(key_list):
  for j, s2 in enumerate(key_list[i+1:]):
    a = positions[s1]
    b = positions[s2]
    m = manhattan(a, b)
    #logging.debug(f"{s1:<3} at {a} to {s2:<3} at {b} is {m}")
    if m > max_distance:
      max_distance = m

logging.info(f"Max distance: {max_distance}")


scanners = parse_scanners(my_input)
logging.debug(f"Resetting {len(scanners)} scanners.")

positions = {"s0": (0,0,0)}
ref_scanner = scanners.pop(0)
ref_scanner.position = [0,0,0]

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
    #logging.debug(f"{s1:<3} at {a} to {s2:<3} at {b} is {m}")
    if m > max_distance:
      max_distance = m

logging.info(f"Max distance: {max_distance}")

