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

def reverse(s):
  return s[::-1]

class Tile:
  def __init__(self, id, lines):
    self.id = id
    self.lines = lines
    self.edges = {}
    self.edges['n'] = lines[0]
    self.edges['s'] = lines[-1]
    self.edges['e'] = ''.join([l[-1] for l in lines])
    self.edges['w'] = ''.join([l[0] for l in lines])

  def edge(self, dir):
    return self.edges[dir]

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

connections = defaultdict(set)

for i in range(len(tiles)):
  i_tile = tiles[i]
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
          connections[i_tile.id].add(j_tile.id)
          connections[j_tile.id].add(i_tile.id)
          side_matches += 1
    if side_matches > 0:
      match_count += 1
  logging.debug("Tile {}={} matches {} tiles.".format(i, i_tile.id, len(connections[i_tile.id])))


product = 1
for tile_id, other_tile_ids in connections.items():
  # corners only connect to two other tiles.
  if len(other_tile_ids) == 2:
    product *= tile_id
logging.info("Part 1: product of corner ids: {}".format(product))