import logging
import re
import sys

from collections import defaultdict

logging.basicConfig(level=logging.DEBUG)

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

class HexTile:
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z
    self.side = WHITE

  def key(self):
    return "{},{},{}".format(self.x, self.y, self.z)

  def flip(self):
    if self.side == WHITE:
      self.side = BLACK
      logging.debug("Flipping tile {} from {} to {}".format(self.key(), WHITE, BLACK))
    else:
      self.side = WHITE
      logging.debug("Flipping tile {} from {} to {}".format(self.key(), BLACK, WHITE))

class HexGrid:
  def __init__(self):
    self.centre = HexTile(0, 0, 0)
    self.all_tiles = {}
    self.all_tiles[self.centre.key()] = self.centre

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

  def flip(self, directions):
    xd, yd, zd = [0, 0, 0]
    for d in directions:
      x, y, z = DIR_COORDS[d]
      xd += x
      yd += y
      zd += z

    t = HexTile(xd, yd, zd)
    tk = t.key()
    if tk in self.all_tiles:
      self.all_tiles[tk].flip()
    else:
      t.flip()
      self.all_tiles[tk] = t

  def print(self):
    for tile in self.all_tiles.values():
      logging.debug("Tile {}: {}".format(tile.key(), tile.side))

grid = HexGrid()

for dir_list in my_input:
  dirs = grid.parse_directions(dir_list)
  grid.flip(dirs)

logging.debug("Grid:")
grid.print()

black_count = 0
for tile in grid.all_tiles.values():
  #tile.print()
  if tile.side == BLACK:
    black_count += 1

logging.info("Part 1: Found {} black tiles".format(black_count))

