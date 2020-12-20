import logging
import math
import re
import sys

from collections import defaultdict

logging.basicConfig(level=logging.DEBUG)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [l.strip() for l in fin.readlines()]

def reverse(s):
  return s[::-1]

class Puzzle:
  def __init__(self, size):
    self.size = size
    self.empty_spaces = size
    self.grid = []
    for i in range(size):
      self.grid.append([None] * size)

  def force_tile(self, tile, x, y):
    if self.grid[x][y] is None:
      self.empty_spaces -= 1
    self.grid[x][y] = tile

  def fit_tile(self, tile):
    pass

class Tile:
  def __init__(self, id, lines):
    self.id = id
    self.lines = lines
    self.edges = {}
    self.compute_edges()

  def compute_edges(self):
    self.edges['n'] = self.lines[0]
    self.edges['s'] = self.lines[-1]
    self.edges['e'] = ''.join([l[-1] for l in self.lines])
    self.edges['w'] = ''.join([l[0] for l in self.lines])

  def edge(self, dir):
    return self.edges[dir]

  def flip_horizontal(self):
    self.lines = [reverse(line) for line in self.lines]
    self.compute_edges()

  def flip_vertical(self):
    self.lines = reverse(self.lines)
    self.compute_edges()

  def rotate(self):
    # abcd    miea
    # efgh -> njfb
    # ijkl    okgc
    # mnop    plhd
    new_lines = []
    for i in range(len(self.lines)):
      new_lines.append(''.join(reverse([l[i] for l in self.lines])))
    self.lines = new_lines
    self.compute_edges

  def print(self):
    logging.debug("Tile {}".format(self.id))
    for line in self.lines:
      logging.debug(line)


# Test tile arrangement:
# 1951    2311    3079
# 2729    1427    2473
# 2971    1489    1171

tiles = list()

tile_lines = list()
tile_id = None
for line in my_input:
  #logging.debug("found a line: {}".format(line))
  if line.startswith("Tile"):
    tile_id = int(line[5:-1])
  elif line == '':
    # create a tile
    tiles.append(Tile(tile_id, tile_lines))
    tile_lines = list()
  else:
    tile_lines.append(line)

if tile_lines:
  tiles.append(Tile(tile_id, tile_lines))

tile_map = {}
connections = defaultdict(set)

for i in range(len(tiles)):
  i_tile = tiles[i]
  tile_map[i_tile.id] = i_tile
  match_count = 0
  for j in range(i+1, len(tiles)):
    j_tile = tiles[j]
    #logging.debug("connecting {}={} and {}={}".format(i, i_tile.id, j, j_tile.id))
    side_matches = 0
    for i_side in ['n', 'e', 'w', 's']:
      i_edge = i_tile.edge(i_side)
      for j_side in ['n', 'e', 'w', 's']:
        j_edge = j_tile.edge(j_side)
        if i_edge == j_edge or i_edge == reverse(j_edge):
          logging.debug('{} side of tile {} matches {} side of tile {}'.format(i_side, i_tile.id, j_side, j_tile.id))
          connections[i_tile.id].add(j_tile)
          connections[j_tile.id].add(i_tile)
          side_matches += 1
    if side_matches > 0:
      match_count += 1
  logging.debug("Tile {}={} matches {} tiles.".format(i, i_tile.id, len(connections[i_tile.id])))

product = 1
corners = []
for tile_id, other_tiles in connections.items():
  # corners only connect to two other tiles.
  if len(other_tiles) == 2:
    product *= tile_id
    corners.append(tile_id)
logging.info("Part 1: product of corner ids: {}".format(product))

def get_a_tile():
  return Tile(25, ['abcd', 'efgh', 'ijkl', 'mnop'])

def test():
  t = get_a_tile()
  logging.debug("Original:")
  t.print()
  logging.debug("Flipped horizontally:")
  t.flip_horizontal()
  t.print()
  t = get_a_tile()
  logging.debug("Flipped vertically:")
  t.flip_vertical()
  t.print()
  t = get_a_tile()
  logging.debug("Rotated once:")
  t.rotate()
  t.print()
  logging.debug("Rotated twice:")
  t.rotate()
  t.print()
  logging.debug("Rotated thrice:")
  t.rotate()
  t.print()
  logging.debug("Rotated 4ice:")
  t.rotate()
  t.print()

#test()

starter = tile_map[corners[0]]
logging.debug("Starting tile:")
starter.print()
p = Puzzle(int(math.sqrt(len(tiles))))
p.force_tile(starter, 0, 0)
for t in connections[starter.id]:
  logging.debug("Fitting next tile:")
  t.print()
