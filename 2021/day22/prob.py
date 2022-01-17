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

consider_min = -50
consider_max = 50


def in_range_one(x):
  return x >= consider_min and x <= consider_max

def in_range(x, y, z):
  return in_range_one(x) and in_range_one(y) and in_range_one(z)

class Cuboid:
  match_expr = re.compile(r"(on|off) x=([0-9-]+)\.\.([0-9-]+),y=([0-9-]+)\.\.([0-9-]+),z=([0-9-]+)\.\.([0-9-]+)")
  def __init__(self, *args):
    if len(args) == 1:
      line = args[0]
      m = Cuboid.match_expr.match(line)
      if m:
        state_text = m.group(1)
        if state_text == 'on':
          self.state = 1
        else:
          self.state = 0
        self.x_min = int(m.group(2))
        self.x_max = int(m.group(3))
        self.y_min = int(m.group(4))
        self.y_max = int(m.group(5))
        self.z_min = int(m.group(6))
        self.z_max = int(m.group(7))
      else:
        logging.warning(f'Could not parse line "{line}"')
    else:
      self.state = args[0]
      self.x_min = args[1]
      self.x_max = args[2]
      self.y_min = args[3]
      self.y_max = args[4]
      self.z_min = args[5]
      self.z_max = args[6]

  def __str__(self):
    return f"{self.state}: ({self.x_min, self.y_min, self.z_min})..({self.x_max, self.y_max, self.z_max}), volume {self.volume()}"

  def set(self, state):
    for x in range(max(self.x_min, consider_min), min(self.x_max, consider_max) + 1):
      for y in range(max(self.y_min, consider_min), min(self.y_max, consider_max) + 1):
        for z in range(max(self.z_min, consider_min), min(self.z_max, consider_max) + 1):
          state[(x, y, z)] = self.state

  def volume(self):
    return (self.x_max - self.x_min) * (self.y_max - self.y_min) * (self.z_max - self.z_min)

  def overlaps_one(self, min1, max1, min2, max2):
    if min2 < min1:
      # make sure the first one is always "left-most" in x terms.
      return self.overlaps_one(min2, max2, min1, max1)
    if max1 <= min2:
      #logging.debug(f"{min1}..{max1} does not overlap {min2}..{max2}")
      return False
    #logging.debug(f"{min1}..{max1} overlaps {min2}..{max2}")
    return True

  def overlaps(self, other):
    x_overlaps = self.overlaps_one(self.x_min, self.x_max, other.x_min, other.x_max)
    y_overlaps = self.overlaps_one(self.y_min, self.y_max, other.y_min, other.y_max)
    z_overlaps = self.overlaps_one(self.z_min, self.z_max, other.z_min, other.z_max)

    return x_overlaps and y_overlaps and z_overlaps


cuboids = []
for line in my_input:
  cuboids.append(Cuboid(line))

#cubes = defaultdict(int)
#for cuboid in cuboids:
#  cuboid.set(cubes)
#
#logging.info(f"cubes on: {sum(cubes.values())}")

# part 2: do it by volume and intersection

applied_cuboids = []

def append_if(list, a, b, x1, x2, y1, y2, z1, z2):
  c = Cuboid(0, x1, x2, y1, y2, z1, z2)
  if c.overlaps(a) or c.overlaps(b):
    if c.volume() > 0:
      list.append(c)

def split_two_overlapping(first, second):
  x1, x2, x3, x4 = sorted([first.x_min, first.x_max, second.x_min, second.x_max])
  y1, y2, y3, y4 = sorted([first.y_min, first.y_max, second.y_min, second.y_max])
  z1, z2, z3, z4 = sorted([first.z_min, first.z_max, second.z_min, second.z_max])

  non_overlapping = []
  # From here, we make a bunch of new non-overlapping cubes, appending
  # only if they have non-zero volume.
  append_if(non_overlapping, first, second, x1, x2, y1, y2, z1, z2)
  append_if(non_overlapping, first, second, x1, x2, y1, y2, z2, z3)
  append_if(non_overlapping, first, second, x1, x2, y1, y2, z3, z4)
  append_if(non_overlapping, first, second, x1, x2, y2, y3, z1, z2)
  append_if(non_overlapping, first, second, x1, x2, y2, y3, z2, z3)
  append_if(non_overlapping, first, second, x1, x2, y2, y3, z3, z4)
  append_if(non_overlapping, first, second, x1, x2, y3, y4, z1, z2)
  append_if(non_overlapping, first, second, x1, x2, y3, y4, z2, z3)
  append_if(non_overlapping, first, second, x1, x2, y3, y4, z3, z4)

  append_if(non_overlapping, first, second, x2, x3, y1, y2, z1, z2)
  append_if(non_overlapping, first, second, x2, x3, y1, y2, z2, z3)
  append_if(non_overlapping, first, second, x2, x3, y1, y2, z3, z4)
  append_if(non_overlapping, first, second, x2, x3, y2, y3, z1, z2)
  append_if(non_overlapping, first, second, x2, x3, y2, y3, z2, z3)
  append_if(non_overlapping, first, second, x2, x3, y2, y3, z3, z4)
  append_if(non_overlapping, first, second, x2, x3, y3, y4, z1, z2)
  append_if(non_overlapping, first, second, x2, x3, y3, y4, z2, z3)
  append_if(non_overlapping, first, second, x2, x3, y3, y4, z3, z4)

  append_if(non_overlapping, first, second, x3, x4, y1, y2, z1, z2)
  append_if(non_overlapping, first, second, x3, x4, y1, y2, z2, z3)
  append_if(non_overlapping, first, second, x3, x4, y1, y2, z3, z4)
  append_if(non_overlapping, first, second, x3, x4, y2, y3, z1, z2)
  append_if(non_overlapping, first, second, x3, x4, y2, y3, z2, z3)
  append_if(non_overlapping, first, second, x3, x4, y2, y3, z3, z4)
  append_if(non_overlapping, first, second, x3, x4, y3, y4, z1, z2)
  append_if(non_overlapping, first, second, x3, x4, y3, y4, z2, z3)
  append_if(non_overlapping, first, second, x3, x4, y3, y4, z3, z4)

  for o in non_overlapping:
    if o.overlaps(first):
      logging.debug(f"{o} overlaps first")
      o.state = first.state
    # second state overrides first state if second is contained within first.
    if o.overlaps(second):
      logging.debug(f"{o} overlaps second")
      o.state = second.state

  # Now put them in the same order as first,second
  if first.state != second.state:
    # Falses come first.
    non_overlapping.sort(key=lambda x: x.state != first.state)
  logging.debug(f"Split {first} and {second} into {len(non_overlapping)} non-overlapping cubes:")
  for no in non_overlapping:
    logging.debug(no)
  # Only keep the "on" cubes
  return [no for no in non_overlapping if no.state]

def reconcile(cuboids):
  logging.debug(f"Attempting to reconcile {len(cuboids)} cuboids")
  if len(cuboids) == 0:
    return []
  if len(cuboids) == 1:
    return cuboids
  if len(cuboids) == 2:
    first, second = cuboids
    return split_two_overlapping(first, second)

  none_overlap = True
  for c1 in cuboids:
    for c2 in cuboids[1:]:
      if c1.overlaps(c2):
        none_overlap = False
        break
  if none_overlap:
    return cuboids

  first = cuboids.pop(0)
  non_overlapping = []
  overlapping = []
  for c in cuboids:
    if first.overlaps(c):
      overlapping.append(c)
    else:
      non_overlapping.append(c)
  de_overlapped = reconcile(overlapping)
  others = reconcile(non_overlapping)
  return de_overlapped + others


## Next attempt:
# if it's an on, find overlapping ons and find the diff, adding only the non-overlapping new on
# if it's an off, find overlapping ons and subtract it from each one, re-adding leftover on bits

for cuboid in cuboids:
  overlapping_cuboids = []
  for ac in applied_cuboids:
    if ac.overlaps(cuboid):
      overlapping_cuboids.append(ac)
  logging.debug(f"Found {len(overlapping_cuboids)} cuboids that overlap {cuboid}")
  for oc in overlapping_cuboids:
    applied_cuboids.remove(oc)
  overlapping_cuboids.append(cuboid)
  reconciled = reconcile(overlapping_cuboids)
  logging.debug(f"Reconciled to {len(reconciled)} cuboids")
  applied_cuboids += reconciled

total_ons = 0
for c in applied_cuboids:
  if c.state == 1:
    total_ons += c.volume()

logging.info(f"Total ons = {total_ons}")

