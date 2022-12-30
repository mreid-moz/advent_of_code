import logging
import re
import sys
from collections import defaultdict

logging.basicConfig(level=logging.INFO)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [l.strip() for l in fin.readlines()]

consider_min = -50
consider_max = 50

def add_if_nonempty(list_of_cuboids, cuboid):
  if cuboid.nonempty():
    logging.debug(f"Adding {cuboid}")
    list_of_cuboids.append(cuboid)
  else:
    logging.debug(f"Skipping empty {cuboid}")

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
    return self.x_max >= self.x_min and self.y_max >= self.y_min and self.z_max >= self.z_min

  def volume(self):
    return (self.x_max - self.x_min + 1) * (self.y_max - self.y_min + 1) * (self.z_max - self.z_min + 1)

  def in_initialization_region(self):
    init_region = Cuboid(1, -50, 50, -50, 50, -50, 50)
    return self.overlaps(init_region)

  def overlaps(self, other):
    i = self.intersect(other)
    return i.nonempty()

  def intersect(self, other, state=1):
    i_x_min = max(other.x_min, self.x_min)
    i_x_max = min(other.x_max, self.x_max)

    i_y_min = max(other.y_min, self.y_min)
    i_y_max = min(other.y_max, self.y_max)

    i_z_min = max(other.z_min, self.z_min)
    i_z_max = min(other.z_max, self.z_max)
    return Cuboid(state, i_x_min, i_x_max, i_y_min, i_y_max, i_z_min, i_z_max)

  def subtract(self, other):
    logging.debug(f"Subtracting {other} from {self}")

    if not self.overlaps(other):
      return [self]

    intersection = self.intersect(other)
    remainder = []

    h = {}
    h['-x'] = {'min': self.x_min, 'max': intersection.x_min - 1}
    h['-y'] = {'min': self.y_min, 'max': intersection.y_min - 1}
    h['-z'] = {'min': self.z_min, 'max': intersection.z_min - 1}

    h['x'] =  {'min': intersection.x_min, 'max': intersection.x_max}
    h['y'] =  {'min': intersection.y_min, 'max': intersection.y_max}
    h['z'] =  {'min': intersection.z_min, 'max': intersection.z_max}

    h['+x'] =  {'min': intersection.x_max + 1, 'max': self.x_max}
    h['+y'] =  {'min': intersection.y_max + 1, 'max': self.y_max}
    h['+z'] =  {'min': intersection.z_max + 1, 'max': self.z_max}

    # Figure out the 26 possible "other" pieces:
    for xk in ['-x','x','+x']:
      for yk in ['-y','y','+y']:
        for zk in ['-z', 'z', '+z']:
          if xk == 'x' and yk == 'y' and zk == 'z':
            continue
          logging.debug(f"Processing sub-cube {xk},{yk},{zk}")
          add_if_nonempty(remainder, Cuboid(self.state, h[xk]['min'], h[xk]['max'], h[yk]['min'], h[yk]['max'], h[zk]['min'], h[zk]['max']))

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

  # This was part 1, but part 2 supercedes it:
  #cubes = defaultdict(int)
  #for cuboid in cuboids:
  #  cuboid.set(cubes)
  #
  #logging.info(f"cubes on: {sum(cubes.values())}")

  # part 2: do it by volume and intersection
  applied_cuboids = [cuboids[0]]
  logging.info(f"Starting with {cuboids[0]}")
  for cuboid in cuboids[1:]:
    logging.info(f"Applying {cuboid}. Volume before: {total_ons(applied_cuboids)} (using {len(applied_cuboids)} cuboids)")

    new_applied_cuboids = []
    for ac in applied_cuboids:
      if ac.overlaps(cuboid):
        logging.debug(f"It overlaps with {ac}")
        i = ac.intersect(cuboid)
        logging.debug(f"Intersection: {i}. breaking down:")
        for sub in ac.subtract(cuboid):
          logging.debug(f"Remainder: {sub}")
          new_applied_cuboids.append(sub)
      else:
        # logging.debug(f"Doesn't overlap with {ac}")
        new_applied_cuboids.append(ac)
    if cuboid.state == 1:
      logging.debug(f"Keeping entire new ON cuboid.")
      new_applied_cuboids.append(cuboid)
    applied_cuboids = new_applied_cuboids
    logging.info(f"Volume after: {total_ons(applied_cuboids)} (using {len(applied_cuboids)} cuboids)")

  logging.info(f"Total ons = {total_ons(applied_cuboids)}")
  logging.info(f"Total ons in init region = {total_ons([c for c in applied_cuboids if c.in_initialization_region()])}")

