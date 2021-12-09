import logging
import copy
import sys
from collections import defaultdict
from functools import reduce

logging.basicConfig(level=logging.INFO)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [[int(c) for c in list(l.strip())] for l in fin.readlines()]

def is_low_point(grid, r, c):
  target = grid[r][c]
  if target == 9:
    return False
  if r > 0:
    if target >= grid[r-1][c]:
      return False
  if c > 0:
    if target >= grid[r][c-1]:
      return False
  if r < len(grid) - 1:
    if target >= grid[r+1][c]:
      return False
  if c < len(grid[0]) - 1:
    if target >= grid[r][c+1]:
      return False
  # Lower than all neighbours
  return True

def get_basin_size(grid, points, points_checked):
  if len(points) == 0:
    logging.debug("Basin contained:")
    for p in set(points_checked):
      logging.debug("  {}".format(p))
    return len(set(points_checked))

  new_points = []
  for r, c in points:
    target = grid[r][c]
    if r > 0:
      if target < grid[r-1][c] and grid[r-1][c] < 9:
        new_points.append((r-1, c))
    if c > 0:
      if target < grid[r][c-1] and grid[r][c-1] < 9:
        new_points.append((r, c-1))
    if r < len(grid) - 1:
      if target < grid[r+1][c] and grid[r+1][c] < 9:
        new_points.append((r+1, c))
    if c < len(grid[0]) - 1:
      if target < grid[r][c+1] and grid[r][c+1] < 9:
        new_points.append((r, c+1))

  return get_basin_size(grid, new_points, points_checked + points)

risk_levels = 0
basin_sizes = []
for row in range(len(my_input)):
  for col in range(len(my_input[0])):
    if is_low_point(my_input, row, col):
      risk_levels += my_input[row][col] + 1
      basin_size = get_basin_size(my_input, [(row,col)], [])
      basin_sizes.append(basin_size)
      logging.debug("Found low point at ({},{}) = {}, basin size {}".format(row, col, my_input[row][col], basin_size))

logging.info("Total of all risk levels is {}".format(risk_levels))
logging.info("Largest basins: {}".format(reduce((lambda x, y: x * y), sorted(basin_sizes)[-3:])))


