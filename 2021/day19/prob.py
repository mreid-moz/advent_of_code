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
      current_scanner = Scanner(line)
      scanners.append(current_scanner)
      continue
    if len(line) == 0:
      continue
    current_scanner.add_line(line)
  return scanners

scanners = parse_scanners(my_input)
logging.debug(f"Found {len(scanners)} scanners.")


orig_scanners = [s for s in scanners]

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

distances = {}

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

#combined = []
#to_be_combined = [s for s inscanners

seeds = combine_scanners(scanners)

while len(seeds) > 1:
  logging.info(f"combining again with {len(seeds)} seeds.")
  seeds = combine_scanners(seeds)

logging.info(f"Part 1: Overall, found {len(seeds[0].beacons)} beacons starting from {seeds[0].name}")

# At this point, are we all in the same orientation? No.

for s1 in orig_scanners:
  offsets = orig_scanners[24].get_offset(s1)
  if offsets is None:
    offsets = orig_scanners[16].get_offset(s1)

  if offsets is None:
    logging.debug(f"Didn't find offsets to 24 or 16 from {s1.name} which had {len(s1.beacons)} beacons and was in orientation {s1.orientation_idx}")

# 24 -> 0         (-53, 1206, 62)
# 24 -> 1         (1112, -4780, -1124)
# 24 -> 2         (-74, -2210, -38)
# 24 -> 3         (2409, -1087, -56)
# 24 -> 4         (-121, -3427, 1283)

# 24 -> 16 -> 5   (1234, -1381, -10)

# 24 -> 6         (36, -4747, -1277)
# 24 -> 7         (-1207, -3541, -1258)
# 24 -> 8         (2396, -2214, -1281)
# 16 -> 9         (2284, 2345, -2355)
# 24 -> 10        (1211, -4624, 16)
# 24 -> 11        (-40, -3544, -1272)
# 24 -> 12        (2355, -2397, 88)
# 24 -> 13        (1243, -1193, -36)
# 24 -> 14        (2274, -3492, 98)
# 24 -> 15        (1139, -2372, -77)

# 16 -> 24        (1232, -48, -51)

# 24 -> 17        (1124, -3492, -60)
# 24 -> 18        (-122, -1041, 14)

# 24 -> 16 -> 19  (2267, 5822, -29)

# 24 -> 20        (-1242, -2240, -1270)
# 24 -> 21        (-110, -3502, 88)
# 24 -> 22        (2344, -3518, 1163)
# 24 -> 23        (1264, -3587, -1221)


# 16 -> 5         (13, -1333, 41)
# 16 -> 19        (1035, 5870, 22)

# 24 -> 5 = (1232, -48, -51) + (13, -1333, 41) = (1234, -1381, -10)

# 24 -> 19 = (1232, -48, -51) + (1035, 5870, 22) = (2267, 5822, -29)

def manhattan(p0, p1=(0,0,0)):
   x0, y0, z0 = p0
   x1, y1, z1 = p1
   return abs(x1 - x0) + abs(y1 - y0) + abs(z1 - z0)

distances = [
  manhattan((-53, 1206, 62)),
  manhattan((1112, -4780, -1124)),
  manhattan((-74, -2210, -38)),
  manhattan((2409, -1087, -56)),
  manhattan((-121, -3427, 1283)),

  manhattan((1232, -48, -51), (13, -1333, 41)),

  manhattan((36, -4747, -1277)),
  manhattan((-1207, -3541, -1258)),
  manhattan((2396, -2214, -1281)),
  manhattan((2284, 2345, -2355)),
  manhattan((1211, -4624, 16)),
  manhattan((-40, -3544, -1272)),
  manhattan((2355, -2397, 88)),
  manhattan((1243, -1193, -36)),
  manhattan((2274, -3492, 98)),
  manhattan((1139, -2372, -77)),

  manhattan((1232, -48, -51)),

  manhattan((1124, -3492, -60)),
  manhattan((-122, -1041, 14)),


  manhattan((1232, -48, -51), (1035, 5870, 22)),

  manhattan((-1242, -2240, -1270)),
  manhattan((-110, -3502, 88)),
  manhattan((2344, -3518, 1163)),
  manhattan((1264, -3587, -1221)),
]

#max_distance = 0
#for i, d1 in enumerate(distances):
#  for j, d2 in enumerate(distances[i+1:]):
#    distance = manhattan(d1, d2)
#    logging.debug(f"Found a distance of {distance}")
#    if distance > max_distance:
#      max_distance = distance

logging.info("Max distance: {}".format(max(distances)))
