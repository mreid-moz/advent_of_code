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

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [l.strip().replace(' ', '') for l in fin.readlines()]

class HexTile:
  def __init__(self, path):
    self.neighbours = defaultdict(HexTile)
    self.side = WHITE
    self.path = path

  def flip(self):
    if self.side == WHITE:
      self.side = BLACK
      logging.debug("Flipping tile {} from {} to {}".format(self.get_path(), WHITE, BLACK))
    else:
      self.side = WHITE
      logging.debug("Flipping tile {} from {} to {}".format(self.get_path(), BLACK, WHITE))

  def get_path(self):
    return ','.join(self.path)

  def print(self, indent=0):
    logging.debug("Path: {}".format(','.join(self.path)))
    logging.debug(" {} {} ".format(self.neighbours.get('nw', HexTile(self.path)).side, self.neighbours.get('ne', HexTile(self.path)).side))
    logging.debug("{} {} {}".format(self.neighbours.get('w', HexTile(self.path)).side, self.side, self.neighbours.get('e', HexTile(self.path)).side))
    logging.debug(" {} {} ".format(self.neighbours.get('sw', HexTile(self.path)).side, self.neighbours.get('se', HexTile(self.path)).side))

class HexGrid:
  def __init__(self):
    self.centre = HexTile([])
    self.all_tiles = {}
    self.all_tiles[self.centre.get_path()] = self.centre

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

  def minify_directions(self, dirs):
    logging.debug("minfying {}".format(','.join(dirs)))
    dir_counts = defaultdict(int)
    for d in dirs:
      dir_counts[d] += 1

    while(dir_counts['e'] > 0 and dir_counts['w'] > 0):
      dir_counts['e'] -= 1
      dir_counts['w'] -= 1
    while(dir_counts['se'] > 0 and dir_counts['nw'] > 0):
      dir_counts['se'] -= 1
      dir_counts['nw'] -= 1
    while(dir_counts['sw'] > 0 and dir_counts['ne'] > 0):
      dir_counts['sw'] -= 1
      dir_counts['ne'] -= 1
    minified = []
    for k in sorted(dir_counts.keys()):
      v = dir_counts[k]
      for i in range(v):
        minified.append(k)
    logging.debug("minified to: {}".format(','.join(minified)))
    return minified

  def flip(self, tile, directions, already_processed_dirs=[]):
    #logging.debug("Flipping tile {} / {}".format(", ".join(already_processed_dirs), ", ".join(directions)))
    if len(directions) == 0:
      tile.flip()
    else:
      d = directions[0]
      if d not in tile.neighbours:
        next_tile = HexTile(already_processed_dirs + [d])
        next_tile.neighbours[RELATIVE_DIRS[d]] = tile
        tile.neighbours[d] = next_tile
        self.all_tiles[next_tile.get_path()] = next_tile
        #next_tile.flip()
      self.flip(tile.neighbours[d], directions[1:], already_processed_dirs + [d])

  def print(self):
    max_path_length = 0
    for tile in self.all_tiles.values():
      if len(tile.path) > max_path_length:
        max_path_length = len(tile.path)

    for i in range(max_path_length + 1):
      #logging.debug("Printing paths of length {}".format(i))
      for k in sorted(self.all_tiles.keys()):
        t = self.all_tiles[k]
        #logging.debug("Key: {}".format(k))
        if len(t.path) == i:
          t.print()


def test():
  hg = HexGrid()
  dirs = hg.parse_directions('esenee')
  assert(dirs == ['e', 'se', 'ne', 'e'])

grid = HexGrid()

for dir_list in my_input:
  dirs = grid.minify_directions(grid.parse_directions(dir_list))
  grid.flip(grid.centre, dirs)

black_count = 0

logging.debug("Grid:")
grid.print()

for tile in grid.all_tiles.values():
  #tile.print()
  if tile.side == BLACK:
    black_count += 1

logging.info("Part 1: Found {} black tiles".format(black_count))

