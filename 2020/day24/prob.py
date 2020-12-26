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
      #logging.debug("Flipping tile {} from {} to {}".format(self.key(), WHITE, BLACK))
    else:
      self.side = WHITE
      #logging.debug("Flipping tile {} from {} to {}".format(self.key(), BLACK, WHITE))

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
    for tile in sorted(self.all_tiles.values(), key=lambda x: x.x * 100000 + x.y * 1000 + x.z):
      logging.debug("Tile {}: {}".format(tile.key(), tile.side))

  def fill_gaps(self):
    min_x = None
    max_x = None
    min_y = None
    max_y = None
    min_z = None
    max_z = None
    for tile in grid.all_tiles.values():
      if min_x is None or tile.x < min_x:
        min_x = tile.x
      if min_y is None or tile.y < min_y:
        min_y = tile.y
      if min_z is None or tile.z < min_z:
        min_z = tile.z

      if max_x is None or tile.x > max_x:
        max_x = tile.x
      if max_y is None or tile.y > max_y:
        max_y = tile.y
      if max_z is None or tile.z > max_z:
        max_z = tile.z

    for x in range(min_x, max_x+1):
      for y in range(min_y, max_y+1):
        for z in range(min_z, max_z+1):
          t = HexTile(x, y, z)
          k = t.key()
          if k not in grid.all_tiles:
            logging.debug("Adding missing tile {}".format(k))
            grid.all_tiles[k] = t
    logging.info("Found {} <= x <= {}, {} <= y <= {}, {} <= z <= {}".format(min_x, max_x, min_y, max_y, min_z, max_z))

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


def day(g):
  flips = set()
  all_values = [v for v in g.all_tiles.values()]
  for t in all_values:
    black_neighbours = 0
    for d, [x, y, z] in DIR_COORDS.items():
      new_tile = HexTile(t.x + x, t.y + y, t.z + z)
      new_key = new_tile.key()
      if new_key in g.all_tiles:
        new_tile = g.all_tiles[new_key]
      else:
        g.all_tiles[new_key] = new_tile
      #logging.debug("Checking {} neighbour of {} tile ({}) -> ({}) which was {}".format(d, t.side, t.key(), new_key, new_tile.side))
      if new_tile.side == BLACK:
        black_neighbours += 1
    if t.side == BLACK and (black_neighbours == 0 or black_neighbours > 2):
      logging.debug("Flipping ({}) from black to white".format(t.key()))
      flips.add(t.key())
    elif t.side == WHITE and black_neighbours == 2:
      logging.debug("Flipping ({}) from white to black".format(t.key()))
      flips.add(t.key())
  logging.debug("Found {} flips.".format(len(flips)))
  for flip in flips:
    g.all_tiles[flip].flip()



for i in range(100):
  #logging.debug("Before day {}:".format(i+1))
  #grid.print()
  grid.fill_gaps()
  day(grid)
  #logging.debug("After day {}:".format(i+1))
  #grid.print()

  black_count = 0
  for tile in grid.all_tiles.values():
    #tile.print()
    if tile.side == BLACK:
      black_count += 1
  logging.info("Processed day {}, found {} black tiles".format(i+1, black_count))



black_count = 0
for tile in grid.all_tiles.values():
  #tile.print()
  if tile.side == BLACK:
    black_count += 1

logging.info("Part 2: Found {} black tiles".format(black_count))

# 4084 is too low.
