import logging
import math
import re
import sys

from collections import defaultdict

logging.basicConfig(level=logging.INFO)

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
    for row in range(self.size):
      spots = []
      for spot in self.grid[row]:
        if spot is None:
          spots.append('____')
        else:
          spots.append(str(spot.id))
      logging.debug(" ".join(spots))

  def force_tile(self, tile, x, y):
    if self.grid[x][y] is None:
      self.empty_spaces -= 1
    self.grid[x][y] = tile

  def fit_tile(self, tile, relative_row, relative_col):
    relative_tile = self.grid[relative_row][relative_col]
    logging.debug("Trying to fit {} relative to {}({},{})".format(tile.id, relative_tile.id, relative_row, relative_col))
    possible_directions = []
    if relative_col - 1 >= 0 and self.grid[relative_row][relative_col - 1] is None:
      possible_directions.append(WEST)
    if relative_col + 1 < self.size and self.grid[relative_row][relative_col + 1] is None:
      possible_directions.append(EAST)
    if relative_row - 1 >= 0 and self.grid[relative_row - 1][relative_col] is None:
      possible_directions.append(NORTH)
    if relative_row + 1 < self.size and self.grid[relative_row + 1][relative_col] is None:
      possible_directions.append(SOUTH)

    if tile is None:
      logging.error("tile is None")
    if relative_tile is None:
      logging.error("relative_tile is None")

    new_tile_row = -1
    new_tile_col = -1
    for i_side in possible_directions:
      logging.debug("Trying to put {} to the {} of {}".format(tile.id, i_side, relative_tile.id))
      i_edge = relative_tile.edge(i_side)
      for j_side in DIRECTIONS:
        j_edge = tile.edge(j_side)
        match = False
        if i_edge == j_edge:
          match = True
          logging.debug('{} side of tile {} matches {} side of tile {}'.format(i_side, relative_tile.id, j_side, tile.id))
          if i_side == EAST:
            new_tile_row = relative_row
            new_tile_col = relative_col + 1
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
            new_tile_row = relative_row - 1
            new_tile_col = relative_col
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
            new_tile_row = relative_row - 1
            new_tile_col = relative_col
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
            new_tile_row = relative_row + 1
            new_tile_col = relative_col
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
              tile.rotate(3)
            elif j_side == SOUTH:
              #  xxx  xxx
              #  xxx  xxx
              #  abc  abc
              tile.flip_vertical()
        elif i_edge == reverse(j_edge):
          match = True
          logging.debug('{} side of tile {} reverse-matches {} side of tile {}'.format(i_side, relative_tile.id, j_side, tile.id))
          # Fix it.
          if i_side == EAST:
            new_tile_row = relative_row
            new_tile_col = relative_col + 1
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
            new_tile_row = relative_row
            new_tile_col = relative_col - 1
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
            new_tile_row = relative_row - 1
            new_tile_col = relative_col
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
            new_tile_row = relative_row + 1
            new_tile_col = relative_col
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
              tile.flip_vertical()
            elif j_side == SOUTH:
              #  xxx  xxx
              #  xxx  xxx
              #  abc  cba
              tile.rotate(2)
        else:
          logging.debug("No match for tile {} {} to tile {} {}".format(relative_tile.id, i_side, tile.id, j_side))

        if match:
          # I think it always fits, but earlier bugs :(
          logging.debug("Looks like we can place {} at ({},{}). Checking neighbours.".format(tile.id, new_tile_row, new_tile_col))
          if self.check_neighbours(tile, new_tile_row, new_tile_col):
            logging.debug("And it fits its neighbours!")
            self.grid[new_tile_row][new_tile_col] = tile
            self.empty_spaces -= 1
          else:
            logging.debug("Sadly it doesn't fit.".format(tile.id, new_tile_row, new_tile_col))
          return new_tile_row, new_tile_col

    if new_tile_row == -1:
      logging.error("Failed to fit tile {} relative to {}".format(tile.id, relative_tile.id))
    return new_tile_row, new_tile_col

  def check_neighbours(self, tile, tile_r, tile_c):
    for x, y, dtile, drel in [
        (tile_r - 1, tile_c,     'n', 's'),
        (tile_r,     tile_c - 1, 'w', 'e'),
        (tile_r,     tile_c + 1, 'e', 'w'),
        (tile_r + 1, tile_c,     's', 'n'),
      ]:
      if x < 0 or x >= self.size or y < 0 or y >= self.size:
        continue
      neighbour = self.grid[x][y]
      if neighbour is None:
        continue
      if tile.edge(dtile) != neighbour.edge(drel):
        logging.debug("Tile {} at ({},{}) would not fit with its neighbour to the {} because '{}' != '{}'".format(tile.id, tile_r, tile_c, dtile, tile.edge(dtile), neighbour.edge(drel)))
        tile.print()
        neighbour.print()
        return False
    return True


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

#test2()

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
placed_tiles.add(starter.id)
while p.empty_spaces > 0:
  relative_tile, row, col = relative_tiles.pop(0)
  # Get these in order of "fewest neighbours"
  for d, t in sorted(connections[relative_tile.id].items(), key=lambda a: len(connections[a[1].id])):
    if t.id in placed_tiles:
      logging.debug("Already placed {}".format(t.id))
      continue
    logging.debug("Fitting next tile {} relative to {}:".format(t.id, relative_tile.id))
    next_row, next_col = p.fit_tile(t, row, col)
    relative_tiles.append([t, next_row, next_col])
    placed_tiles.add(t.id)
    p.print()

p.print()

big_picture = []
for row in range(p.size):
  for col in range(p.size):
    t = p.grid[row][col]
    logging.debug("Appending tile ({},{}):".format(row, col))
    t.print()

    # trim the edges
    t_lines = [line[1:-1] for line in t.lines]
    t_lines.pop(0)
    t_lines.pop()
    for i, line in enumerate(t_lines):
      if col == 0:
        big_picture.append(line)
      else:
        big_picture[row*len(t_lines)+i] += line

logging.debug("Big picture:")
for line in big_picture:
  logging.debug(" {}".format(line))

class Matrix:
  def __init__(self, lines):
    self.lines = lines

  def print(self):
    for line in self.lines:
      logging.debug(line)

  def print_corners(self):
    logging.debug("{}...{}".format(self.lines[0][0], self.lines[0][-1]))
    logging.debug("{}...{}".format(self.lines[-1][0], self.lines[-1][-1]))

  def find(self, other_matrix):
    width = len(self.lines[0])
    height = len(self.lines)
    o_width = len(other_matrix.lines[0])
    o_height = len(other_matrix.lines)
    for row in range(height - o_height):
      for col in range(width - o_width):
        found_all = True
        for i, line in enumerate(other_matrix.lines):
          if self.lines[row][col:].startswith(line):
            logging.debug("Found '{}' in line {}='{}' at offset {}".format(line, row, self.lines[row], col))
          else:
            logging.debug("Didn't find '{}' in line {}='{}'".format(line, row, self.lines[row]))
            found_all = False
            break
        if found_all:
          logging.debug("Found at ({},{})".format(col, row))
          return row, col
    return None, None

  def find_all(self, needle):
    coords = []
    for row in range(len(self.lines)):
      for col in range(len(self.lines[0])):
        if self.lines[row][col] == needle:
          coords.append([row, col])
    return coords

  def count(self, needle):
    total = 0
    for row in range(len(self.lines)):
      for col in range(len(self.lines[0])):
        if self.lines[row][col] == needle:
          total += 1
    return total

  def match_coords(self, match_char, coords, relative_row, relative_col):
    for row, col in coords:
      if self.lines[row+relative_row][col+relative_col] != match_char:
        return False
    return True

  def update_coords(self, coords, replacement_char, relative_row, relative_col):
    for r, c in coords:
      row = relative_row + r
      col = relative_col + c
      self.lines[row] = self.lines[row][:col] + replacement_char + self.lines[row][col+1:]

  def mask(self, other_matrix, mask_char='#', replace_char='O'):
    mask_coords = other_matrix.find_all(mask_char)

    width = len(self.lines[0])
    height = len(self.lines)
    o_width = len(other_matrix.lines[0])
    o_height = len(other_matrix.lines)

    match_count = 0
    for row in range(height - o_height):
      for col in range(width - o_width):
        if self.match_coords(mask_char, mask_coords, row, col):
          self.update_coords(mask_coords, replace_char, row, col)
          match_count += 1
    return match_count

  def flip_horizontal(self):
    self.lines = [reverse(line) for line in self.lines]

  def flip_vertical(self):
    self.lines = reverse(self.lines)

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

def test2():
  m = [
    'aaaaa',
    'abbba',
    'abbba',
    'aaaaa',
    'aaaaa',
  ]
  om = [
   'bbb',
   'bbb'
  ]

  matrix = Matrix(m)
  other = Matrix(om)

  x, y = matrix.find(other)
  assert(x == 1 and y == 1)

  om2 = [
   'bbb',
   'bbc'
  ]

  row, col = matrix.find(Matrix(om2))
  assert(row is None and row is None)

#test2()

bp = Matrix(big_picture)

sea_monster_lines = [
  '                  # ',
  '#    ##    ##    ###',
  ' #  #  #  #  #  #   '
]

monster_matrix = Matrix(sea_monster_lines)

monster_coords = monster_matrix.find_all('#')
logging.debug("Monster coords: {}".format(monster_coords))

def try_flips(matrix, mask):
  logging.debug("Trying flips... initial state:")
  matrix.print_corners()
  replace_count = matrix.mask(mask)
  if replace_count == 0:
    matrix.flip_horizontal()
    logging.debug("Trying flips... after h flip:")
    matrix.print_corners()
    replace_count = matrix.mask(mask)
    logging.debug("replace count = {}".format(replace_count))
    if replace_count == 0:
      matrix.flip_horizontal()
      matrix.flip_vertical()
      logging.debug("Trying flips... after v flip:")
      matrix.print_corners()
      replace_count = matrix.mask(mask)
      if replace_count == 0:
        matrix.flip_vertical()
  return replace_count

replace_count = try_flips(bp, monster_matrix)
if replace_count == 0:
  bp.rotate() # now 90
  replace_count = try_flips(bp, monster_matrix)
  if replace_count == 0:
    bp.rotate() # now 180
    replace_count = try_flips(bp, monster_matrix)
    if replace_count == 0:
      bp.rotate() # now 270
      replace_count = try_flips(bp, monster_matrix)

#bp.print()

logging.info("Part 2: water roughness {}".format(bp.count('#')))
