import logging
import re
import sys

from collections import defaultdict

logging.basicConfig(level=logging.INFO)

WHITE = 'w'
BLACK = 'b'
DIRECTIONS = set(['e', 'se', 'sw', 'w', 'nw', 'ne'])
RELATIVE_DIRS = {
  'e': 'w',
  'w': 'e',
  'ne': 'sw',
  'se': 'nw',
  'sw': 'ne',
  'nw': 'se',
}
DIR_COORDS = {
  # d:  [ x,  y,  z]
  'e':  [ 1, -1,  0],
  'w':  [-1,  1,  0],
  'ne': [ 1,  0, -1],
  'nw': [ 0,  1, -1],
  'se': [ 0, -1,  1],
  'sw': [-1,  0,  1]
}

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [l.strip().replace(' ', '') for l in fin.readlines()]

class HexGrid:
  def __init__(self):
    self.half_n = 120
    n = self.half_n * 2
    self.tiles = [[[False for k in range(n)] for j in range(n)] for i in range(n)]
    self.black_tile_count = 0
    self.min_flipped_x = None
    self.min_flipped_y = None
    self.min_flipped_z = None
    self.max_flipped_x = None
    self.max_flipped_y = None
    self.max_flipped_z = None

  def parse_directions(self, dir_str):
    dir_list = list(dir_str)
    dirs = []
    c = ''
    while len(dir_list):
      c += dir_list.pop(0)
      if c in DIRECTIONS:
        dirs.append(c)
        c = ''
    if len(c) > 0:
      dirs.append(c)
    return dirs

  def get_offset(self, x, y, z):
    return [x + self.half_n, y + self.half_n, z + self.half_n]

  def get_value(self, rx, ry, rz):
    x, y, z = self.get_offset(rx, ry, rz)
    return self.tiles[x][y][z]

  def set_value(self, rx, ry, rz, v):
    x, y, z = self.get_offset(rx, ry, rz)
    self.tiles[x][y][z] = v

  def flip(self, dir_list):
    directions = self.parse_directions(dir_list)
    xd, yd, zd = [0, 0, 0]
    for d in directions:
      x, y, z = DIR_COORDS[d]
      xd += x
      yd += y
      zd += z
    self.flip_one(xd, yd, zd)

  def flip_one(self, xd, yd, zd):
    if self.min_flipped_x is None or xd < self.min_flipped_x:
      self.min_flipped_x = xd
    if self.min_flipped_y is None or yd < self.min_flipped_y:
      self.min_flipped_y = yd
    if self.min_flipped_z is None or zd < self.min_flipped_z:
      self.min_flipped_z = zd
    if self.max_flipped_x is None or xd > self.max_flipped_x:
      self.max_flipped_x = xd
    if self.max_flipped_y is None or yd > self.max_flipped_y:
      self.max_flipped_y = yd
    if self.max_flipped_z is None or zd > self.max_flipped_z:
      self.max_flipped_z = zd

    v = self.get_value(xd, yd, zd)
    if v:
      self.black_tile_count -= 1
    else:
      self.black_tile_count += 1

    self.set_value(xd, yd, zd, not v)

logging.debug("Initializing...")
grid = HexGrid()
logging.debug("Done initializing.")

for dir_list in my_input:
  grid.flip(dir_list)

logging.info("Part 1: Found {} black tiles".format(grid.black_tile_count))


def day(g):
  flips = []
  for x in range(g.min_flipped_x - 1, g.max_flipped_x + 2):
    for y in range(g.min_flipped_y - 1, g.max_flipped_y + 2):
      for z in range(g.min_flipped_z - 1, g.max_flipped_z + 2):
        v = g.get_value(x, y, z)
        #logging.debug("Checking ({},{},{}), current value is {}".format(x, y, z, v))
        black_neighbours = 0
        for [xd, yd, zd] in DIR_COORDS.values():
          nv = g.get_value(x+xd, y+yd, z+zd)
          if nv:
            black_neighbours += 1
        if v and (black_neighbours == 0 or black_neighbours > 2):
          logging.debug("Flipping ({},{},{}) from black to white".format(x, y, z))
          flips.append([x, y, z])
        elif not v and black_neighbours == 2:
          logging.debug("Flipping ({},{},{}) from white to black".format(x, y, z))
          flips.append([x, y, z])

  logging.debug("Found {} flips.".format(len(flips)))
  for x, y, z in flips:
    g.flip_one(x, y, z)



for i in range(100):
  day(grid)
  logging.info("Processed day {}, found {} black tiles".format(i+1, grid.black_tile_count))

logging.info("Part 2: Found {} black tiles".format(grid.black_tile_count))

# 4084 is too low.
