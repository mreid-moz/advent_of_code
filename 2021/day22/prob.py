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
  MATCH_EXPR = re.compile(r"(on|off) x=([0-9-]+)\.\.([0-9-]+),y=([0-9-]+)\.\.([0-9-]+),z=([0-9-]+)\.\.([0-9-]+)")
  def __init__(self, *args):
    if len(args) == 1:
      line = args[0]
      m = Cuboid.MATCH_EXPR.match(line)
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
    state_str = 'OFF'
    if self.state == 1:
      state_str = 'ON'
    return f"{state_str}: ({self.x_min, self.y_min, self.z_min})..({self.x_max, self.y_max, self.z_max}), volume {self.volume()}"

  def set(self, state):
    for x in range(max(self.x_min, consider_min), min(self.x_max, consider_max) + 1):
      for y in range(max(self.y_min, consider_min), min(self.y_max, consider_max) + 1):
        for z in range(max(self.z_min, consider_min), min(self.z_max, consider_max) + 1):
          state[(x, y, z)] = self.state

  def nonempty(self):
    return self.x_max > self.x_min and self.y_max > self.y_min and self.z_max > self.z_min

  def volume(self):
    return (self.x_max - self.x_min + 1) * (self.y_max - self.y_min + 1) * (self.z_max - self.z_min + 1)

  def overlaps_one(self, min1, max1, min2, max2):
    if min2 < min1:
      # make sure the first one is always "left-most" in x terms.
      return self.overlaps_one(min2, max2, min1, max1)
    if max1 <= min2:
      #logging.debug(f"{min1}..{max1} does not overlap {min2}..{max2}")
      return False
    #logging.debug(f"{min1}..{max1} overlaps {min2}..{max2}")
    return True

  def in_initialization_region(self):
    init_region = Cuboid(1, -50, 50, -50, 50, -50, 50)
    return self.overlaps(init_region)

  def overlaps(self, other):
    i = self.intersect(other)
    return i.nonempty()

    # x_overlaps = self.overlaps_one(self.x_min, self.x_max, other.x_min, other.x_max)
    # y_overlaps = self.overlaps_one(self.y_min, self.y_max, other.y_min, other.y_max)
    # z_overlaps = self.overlaps_one(self.z_min, self.z_max, other.z_min, other.z_max)

    # return x_overlaps and y_overlaps and z_overlaps

  def intersect(self, other, state=1):
    i_x_min = max(other.x_min, self.x_min)
    i_x_max = min(other.x_max, self.x_max)

    i_y_min = max(other.y_min, self.y_min)
    i_y_max = min(other.y_max, self.y_max)

    i_z_min = max(other.z_min, self.z_min)
    i_z_max = min(other.z_max, self.z_max)
    return Cuboid(state, i_x_min, i_x_max, i_y_min, i_y_max, i_z_min, i_z_max)

  SUB_GRID = [ ((0,1),(0,1),(0,1)), ((1,2),(0,1),(0,1)), ((2,3),(0,1),(0,1)),
               ((0,1),(1,2),(0,1)), ((1,2),(1,2),(0,1)), ((2,3),(1,2),(0,1)),
               ((0,1),(2,3),(0,1)), ((1,2),(2,3),(0,1)), ((2,3),(2,3),(0,1)),

               ((0,1),(0,1),(1,2)), ((1,2),(0,1),(1,2)), ((2,3),(0,1),(1,2)),
               ((0,1),(1,2),(1,2)), ((1,2),(1,2),(1,2)), ((2,3),(1,2),(1,2)),
               ((0,1),(2,3),(1,2)), ((1,2),(2,3),(1,2)), ((2,3),(2,3),(1,2)),

               ((0,1),(0,1),(2,3)), ((1,2),(0,1),(2,3)), ((2,3),(0,1),(2,3)),
               ((0,1),(1,2),(2,3)), ((1,2),(1,2),(2,3)), ((2,3),(1,2),(2,3)),
               ((0,1),(2,3),(2,3)), ((1,2),(2,3),(2,3)), ((2,3),(2,3),(2,3)) ]

  def subtract(self, other):
    # if other.state == self.state:
    #   return [self]

    if not self.overlaps(other):
      return [self]

    # the bounding box is:
    x_sorted = sorted([other.x_min, other.x_max, self.x_min, self.x_max])
    y_sorted = sorted([other.y_min, other.y_max, self.y_min, self.y_max])
    z_sorted = sorted([other.z_min, other.z_max, self.z_min, self.z_max])

    x_ranges = [(x_sorted[0], x_sorted[1] - 1), (x_sorted[1], x_sorted[2] - 1), (x_sorted[2], x_sorted[3])]
    y_ranges = [(y_sorted[0], y_sorted[1] - 1), (y_sorted[1], y_sorted[2] - 1), (y_sorted[2], y_sorted[3])]
    z_ranges = [(z_sorted[0], z_sorted[1] - 1), (z_sorted[1], z_sorted[2] - 1), (z_sorted[2], z_sorted[3])]

    remainder = []

    for (x_min, x_max) in x_ranges:
      for (y_min, y_max) in y_ranges:
        for (z_min, z_max) in z_ranges:
    # for ((xi0,xi1),(yi0,yi1),(zi0,zi1)) in Cuboid.SUB_GRID:
    #   x_min = x_sorted[xi0]
    #   x_max = x_sorted[xi1]
    #   y_min = y_sorted[yi0]
    #   y_max = y_sorted[yi1]
    #   z_min = z_sorted[zi0]
    #   z_max = z_sorted[zi1]
          c = Cuboid(self.state, x_min, x_max, y_min, y_max, z_min, z_max)
          if c.nonempty() and self.overlaps(c) and not other.overlaps(c):
            remainder.append(c)
    return remainder

def total_ons(cuboids):
  ons = 0
  for c in cuboids:
    if c.state == 1:
      ons += c.volume()
  return ons


if __name__ == "__main__":
  cuboids = []
  for line in my_input:
    if line.startswith('#'):
      continue
    cuboids.append(Cuboid(line))

  #cubes = defaultdict(int)
  #for cuboid in cuboids:
  #  cuboid.set(cubes)
  #
  #logging.info(f"cubes on: {sum(cubes.values())}")

  # part 2: do it by volume and intersection
  ## Next attempt:
  # if it's an on, find overlapping ons and find the diff, adding only the non-overlapping new on
  # if it's an off, find overlapping ons and subtract it from each one, re-adding leftover on bits
  applied_cuboids = [cuboids[0]]
  logging.info(f"Starting with {cuboids[0]}")
  for cuboid in cuboids[1:]:
    logging.info(f"Applying {cuboid}. Volume before: {total_ons(applied_cuboids)} (using {len(applied_cuboids)} cuboids)")

    new_applied_cuboids = []
    for ac in applied_cuboids:
      if ac.overlaps(cuboid):
        logging.info(f"It overlaps with {ac}")
        i = ac.intersect(cuboid)
        logging.debug(f"Intersection: {i}. breaking down:")
        for sub in ac.subtract(cuboid):
          logging.debug(f"Remainder: {sub}")
          new_applied_cuboids.append(sub)
        # overlapping_cuboids.append(ac)
      else:
        # logging.debug(f"Doesn't overlap with {ac}")
        new_applied_cuboids.append(ac)
    if cuboid.state == 1:
      logging.debug(f"Keeping entire new ON cuboid.")
      new_applied_cuboids.append(cuboid)
    applied_cuboids = new_applied_cuboids
    logging.info(f"Volume after: {total_ons(applied_cuboids)} (using {len(applied_cuboids)} cuboids)")

  # total_ons = 0
  # for c in applied_cuboids:
  #   if c.state == 1:
  #     total_ons += c.volume()

  logging.info(f"Total ons = {total_ons(applied_cuboids)}")

  logging.info(f"Total ons in init region = {total_ons([c for c in applied_cuboids if c.in_initialization_region()])}")

