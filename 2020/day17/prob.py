import logging
import re
import sys
from copy import deepcopy

logging.basicConfig(level=logging.INFO)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [list(l.strip()) for l in fin.readlines()]

def get_key(x, y, z):
  return "{},{},{}".format(x, y, z)

def initialize(square):
  cube = {}
  size = len(square)
  for x in range(size):
    for y in range(size):
      coord = get_key(x, y, 0)
      cube[coord] = square[x][y]
  return cube

def grow(cube, new_xy_size, new_z_size):
  for x in range(-new_z_size, new_xy_size):
    for y in range(-new_z_size, new_xy_size):
      for z in range(-new_z_size, new_z_size+1):
        coord = get_key(x, y, z)
        if coord not in cube:
          #logging.debug("Growing: filling out location {}".format(coord))
          cube[coord] = '.'

def valid_position(cube, x, y, z):
  return get_key(x, y, z) in cube

def update_cubes(cube, xy_size, z_size):
  updated_cube = deepcopy(cube)
  for x in range(-z_size, xy_size):
    for y in range(-z_size, xy_size):
      for z in range(-z_size, z_size+1):
        k = get_key(x, y, z)
        #logging.debug("Updating ({})".format(k))
        updated_cube[k] = update_location(cube, x, y, z)
  return updated_cube

def update_location(cube, x, y, z):
  active_neighbours = 0
  current_key = get_key(x, y, z)
  current_state = cube[current_key]
  for xn in [x-1, x, x+1]:
    for yn in [y-1, y, y+1]:
      for zn in [z-1, z, z+1]:
        if x == xn and y == yn and z == zn:
          continue # it's a me!
        if not valid_position(cube, xn, yn, zn):
          continue
        neighbour_value = cube[get_key(xn, yn, zn)]
        if neighbour_value == '#':
          #logging.debug("relative to {}, {} was active".format(current_key, get_key(xn, yn, zn)))
          active_neighbours += 1
  #logging.debug("Looking at neighbours of {}, {} were active".format(current_key, active_neighbours))
  if current_state == '#' and active_neighbours not in [2,3]:
    logging.debug("Flipping {} from active to inactive because it had {} active neighbours".format(current_key, active_neighbours))
    return '.'
  if current_state == '.' and active_neighbours == 3:
    logging.debug("Flipping {} from inactive to active because it had {} active neighbours".format(current_key, active_neighbours))
    return '#'
  return current_state


def print_cube(cube, xy_size, z_size):
  for z in range(-z_size, z_size+1):
    print("z = {}".format(z))
    for x in range(-z_size, xy_size):
      row = []
      for y in range(-z_size, xy_size):
        k = get_key(x, y, z)
        #logging.debug("getting {}".format(k))
        row.append(cube[k])
      print("r{}:  {}".format(x, "".join(row)))
    print()

def count_active(cube):
  count = 0
  for v in cube.values():
    if v == '#':
      count += 1
  return count


round_count = 0
cube = initialize(my_input)
xy_size = len(my_input)
z_size = 0
logging.info("After {} rounds:".format(round_count))
print_cube(cube, xy_size, z_size)
for i in range(6):
  z_size += 1
  xy_size += 1
  grow(cube, xy_size, z_size)
  cube = update_cubes(cube, xy_size, z_size)
  round_count += 1
  logging.info("After {} rounds:".format(round_count))
  print_cube(cube, xy_size, z_size)

logging.info("Part 1: After {} rounds, there were {} active cubes".format(round_count, count_active(cube)))
