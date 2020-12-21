import logging
import math
import re
import sys

from collections import defaultdict

logging.basicConfig(level=logging.DEBUG)

NORTH = 'n'
EAST  = 'e'
WEST  = 'w'
SOUTH = 's'
DIRECTIONS = [NORTH, EAST, WEST, SOUTH]

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
    self.empty_spaces = size * size
    self.grid = []
    for i in range(size):
      self.grid.append([None] * size)

  def print(self):
    logging.debug("Puzzle state:")
    for x in range(self.size):
      spots = []
      for spot in self.grid[x]:
        if spot is None:
          spots.append('____')
        else:
          spots.append(str(spot.id))
      logging.debug(" ".join(spots))

  def force_tile(self, tile, x, y):
    if self.grid[x][y] is None:
      self.empty_spaces -= 1
    self.grid[x][y] = tile

  def fit_tile(self, tile, relative_x, relative_y):
    relative_tile = self.grid[relative_x][relative_y]
    possible_directions = []
    if relative_x - 1 >= 0 and self.grid[relative_x - 1][relative_y] is None:
      possible_directions.append(WEST)
    if relative_x + 1 < self.size and self.grid[relative_x + 1][relative_y] is None:
      possible_directions.append(EAST)
    if relative_y - 1 >= 0 and self.grid[relative_x][relative_y - 1] is None:
      possible_directions.append(NORTH)
    if relative_y + 1 < self.size and self.grid[relative_x][relative_y + 1] is None:
      possible_directions.append(SOUTH)

    if tile is None:
      logging.error("tile is None")
    if relative_tile is None:
      logging.error("relative_tile is None")

    new_tile_x = -1
    new_tile_y = -1
    for i_side in possible_directions:
      logging.debug("Trying to put {} to the {} of {}".format(tile.id, i_side, relative_tile.id))
      i_edge = relative_tile.edge(i_side)
      for j_side in DIRECTIONS:
        j_edge = tile.edge(j_side)
        match = False
        if i_edge == j_edge:
          match = True
          logging.debug('{} side of tile {} matches {} side of tile {}'.format(i_side, relative_tile.id, j_side, tile.id))
          relative_tile.print()
          tile.print()
          if i_side == EAST:
            new_tile_x = relative_x + 1
            new_tile_y = relative_y
            if j_side == NORTH:
              #  xxa  abc
              #  xxb  xxx
              #  xxc  xxx
              tile.rotate()
              tile.flip_horizontal()
            elif j_side == EAST:
              #  xxa  xxa
              #  xxb  xxb
              #  xxc  xxc
              tile.flip_horizontal()
            elif j_side == SOUTH:
              #  xxa  xxx
              #  xxb  xxx
              #  xxc  abc
              tile.rotate()
          elif i_side == WEST:
            new_tile_x = relative_x - 1
            new_tile_y = relative_y
            if j_side == WEST:
              #  axx  axx
              #  bxx  bxx
              #  cxx  cxx
              tile.flip_horizontal()
            elif j_side == NORTH:
              #  axx  abc
              #  bxx  xxx
              #  cxx  xxx
              tile.rotate()
            elif j_side == SOUTH:
              #  axx  xxx
              #  bxx  xxx
              #  cxx  abc
              tile.rotate()
              tile.flip_horizontal()
          elif i_side == NORTH:
            new_tile_x = relative_x
            new_tile_y = relative_y - 1
            if j_side == WEST:
              #  abc  axx
              #  xxx  bxx
              #  xxx  cxx
              tile.rotate()
              tile.flip_vertical()
            elif j_side == NORTH:
              #  abc  abc
              #  xxx  xxx
              #  xxx  xxx
              tile.flip_vertical()
            elif j_side == EAST:
              #  abc  xxa
              #  xxx  xxb
              #  xxx  xxc
              tile.rotate()
              tile.flip_horizontal()
          else: # i_side == SOUTH:
            new_tile_x = relative_x
            new_tile_y = relative_y + 1
            if j_side == WEST:
              #  xxx  axx
              #  xxx  bxx
              #  abc  cxx
              tile.rotate()
              tile.flip_horizontal()
            elif j_side == EAST:
              #  xxx  xxa
              #  xxx  xxb
              #  abc  xxc
              tile.rotate()
              tile.flip_horizontal()
            elif j_side == SOUTH:
              #  xxx  xxx
              #  xxx  xxx
              #  abc  abc
              tile.flip_vertical()
        elif i_edge == reverse(j_edge):
          match = True
          logging.debug('{} side of tile {} reverse-matches {} side of tile {}'.format(i_side, relative_tile.id, j_side, tile.id))
          relative_tile.print()
          tile.print()
          # Fix it.
          if i_side == EAST:
            new_tile_x = relative_x + 1
            new_tile_y = relative_y
            if j_side == WEST:
              #  xxa  cxx
              #  xxb  bxx
              #  xxc  axx
              tile.flip_vertical()
            elif j_side == NORTH:
              #  xxa  cba
              #  xxb  xxx
              #  xxc  xxx
              tile.rotate(3)
            elif j_side == EAST:
              #  xxa  xxc
              #  xxb  xxb
              #  xxc  xxa
              tile.rotate(2)
            elif j_side == SOUTH:
              #  xxa  xxx
              #  xxb  xxx
              #  xxc  cba
              tile.rotate()
              tile.flip_vertical()
          elif i_side == WEST:
            new_tile_x = relative_x - 1
            new_tile_y = relative_y
            if j_side == WEST:
              #  axx  cxx
              #  bxx  bxx
              #  cxx  axx
              tile.rotate(2)
            elif j_side == NORTH:
              #  axx  cba
              #  bxx  xxx
              #  cxx  xxx
              tile.rotate()
              tile.flip_vertical()
            elif j_side == EAST:
              #  axx  xxc
              #  bxx  xxb
              #  cxx  xxa
              tile.flip_vertical()
            elif j_side == SOUTH:
              #  axx  xxx
              #  bxx  xxx
              #  cxx  cba
              tile.rotate()
              tile.flip_vertical()
          elif i_side == NORTH:
            new_tile_x = relative_x
            new_tile_y = relative_y - 1
            if j_side == WEST:
              #  abc  cxx
              #  xxx  bxx
              #  xxx  axx
              tile.rotate()
              tile.flip_vertical()
            elif j_side == NORTH:
              #  abc  cba
              #  xxx  xxx
              #  xxx  xxx
              tile.rotate(2)
            elif j_side == EAST:
              #  abc  xxc
              #  xxx  xxb
              #  xxx  xxa
              tile.rotate()
            elif j_side == SOUTH:
              #  abc  xxx
              #  xxx  xxx
              #  xxx  cba
              tile.flip_horizontal()
          else: # i_side == SOUTH:
            new_tile_x = relative_x
            new_tile_y = relative_y + 1
            if j_side == WEST:
              #  xxx  cxx
              #  xxx  bxx
              #  abc  axx
              tile.rotate()
            elif j_side == NORTH:
              #  xxx  cba
              #  xxx  xxx
              #  abc  xxx
              tile.flip_horizontal()
            elif j_side == EAST:
              #  xxx  xxc
              #  xxx  xxb
              #  abc  xxa
              tile.rotate()
              tile.flip_horizontal()
            elif j_side == SOUTH:
              #  xxx  xxx
              #  xxx  xxx
              #  abc  cba
              tile.rotate(2)
        if match:
          # TODO: check neighbours before we commit.
          self.grid[new_tile_x][new_tile_y] = tile
          self.empty_spaces -= 1
          logging.debug("After re-orienting the tiles:")
          relative_tile.print()
          tile.print()
          return new_tile_x, new_tile_y
    if new_tile_x == -1:
      logging.error("Failed to fit tile {} relative to {}".format(tile.id, relative_tile.id))
    return new_tile_x, new_tile_y



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

  # 90 degrees clockwise
  def rotate(self, times=1):
    # abcd    miea
    # efgh -> njfb
    # ijkl    okgc
    # mnop    plhd
    for i in range(times):
      new_lines = []
      for i in range(len(self.lines)):
        new_lines.append(''.join(reverse([l[i] for l in self.lines])))
      self.lines = new_lines
    self.compute_edges()

  def print(self):
    logging.debug("Tile {}".format(self.id))
    for line in self.lines:
      logging.debug(line)


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
connections = defaultdict(dict)

for i in range(len(tiles)):
  i_tile = tiles[i]
  tile_map[i_tile.id] = i_tile
  match_count = 0
  for j in range(i+1, len(tiles)):
    j_tile = tiles[j]
    #logging.debug("connecting {}={} and {}={}".format(i, i_tile.id, j, j_tile.id))
    side_matches = 0
    for i_side in DIRECTIONS:
      i_edge = i_tile.edge(i_side)
      for j_side in DIRECTIONS:
        j_edge = j_tile.edge(j_side)
        if i_edge == j_edge:
          logging.debug('{} side of tile {} matches {} side of tile {}'.format(i_side, i_tile.id, j_side, j_tile.id))
          connections[i_tile.id][i_side] = j_tile
          connections[j_tile.id][j_side] = i_tile
          side_matches += 1
        elif i_edge == reverse(j_edge):
          logging.debug('{} side of tile {} reverse-matches {} side of tile {}'.format(i_side, i_tile.id, j_side, j_tile.id))
          connections[i_tile.id][i_side] = j_tile
          connections[j_tile.id][j_side] = i_tile
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

directions = sorted(connections[starter.id].keys())
#   It needs to be ['e', 's'] to live in the top left corner.
if   directions == ['e', 'n']:
  starter.flip_vertical()
elif directions == ['s', 'w']:
  starter.flip_horizontal()
elif directions == ['n', 'w']:
  starter.flip_horizontal()
  starter.flip_vertical()
logging.debug("After reorienting:")
starter.print()

p = Puzzle(int(math.sqrt(len(tiles))))
p.force_tile(starter, 0, 0)
relative_tiles = [[starter, 0, 0]]
placed_tiles = set()
while p.empty_spaces > 0:
  relative_tile, x, y = relative_tiles.pop(0)
  for d, t in connections[relative_tile.id].items():
    if t.id in placed_tiles:
      logging.debug("Already placed {}".format(t.id))
      continue
    logging.debug("Fitting next tile {} relative to {}:".format(t.id, relative_tile.id))
    next_x, next_y = p.fit_tile(t, x, y)
    relative_tiles.append([t, next_x, next_y])
    placed_tiles.add(t.id)
    p.print()

p.print()

big_picture = []
for x in range(p.size):
  #big_picture.append([''] * p.size)
  for y in range(p.size):
    t = p.grid[x][y]
    logging.debug("Appending tile ({},{}):".format(x, y))
    t.print()

    # Debugging:
    #t.lines[3] = t.lines[3][0:3] + str(t.id) + t.lines[3][7:]

    # trim the edges
    t_lines = [line[1:-1] for line in t.lines]
    t_lines.pop(0)
    t_lines.pop()
    for i, line in enumerate(t_lines):
      if y == 0:
        big_picture.append(line)
      else:
        big_picture[x*len(t_lines)+i] += line

logging.debug("Big picture:")
for line in big_picture:
  logging.debug(" {}".format(line))

