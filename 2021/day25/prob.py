import logging
import re
import sys
from collections import defaultdict, deque
import copy

logging.basicConfig(level=logging.INFO)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [list(l.strip()) for l in fin.readlines()]

def empty(grid, r, c):
  return grid[r][c] == '.'

def step_east(grid):
  moves = 0
  new_grid = []
  for r in range(len(grid)):
    new_grid.append(['.'] * len(grid[0]))

  for r in range(len(grid)):
    for c in range(len(grid[0])):
      cuke = grid[r][c]
      if cuke == '.':
        continue
      if cuke == 'v':
        new_grid[r][c] = cuke
        continue

      n_c = (c+1) % len(grid[0])
      if grid[r][n_c] == '.':
        moves += 1
        logging.debug(f"moving {cuke} east from col {c} {n_c}")
      else:
        logging.debug(f"Couldn't move {cuke} from ({r},{c})")
        n_c = c
      new_grid[r][n_c] = cuke
  return moves, new_grid

def step_south(grid):
  moves = 0
  new_grid = []
  for r in range(len(grid)):
    new_grid.append(['.'] * len(grid[0]))

  for r in range(len(grid)):
    for c in range(len(grid[0])):
      cuke = grid[r][c]
      if cuke == '.':
        continue
      if cuke == '>':
        new_grid[r][c] = cuke
        continue

      n_r = (r+1) % len(grid)
      if grid[n_r][c] == '.':
        moves += 1
        logging.debug(f"moving {cuke} south from row {r} to {n_r}")
      else:
        logging.debug(f"Couldn't move {cuke} from ({r},{c})")
        n_r = r
      new_grid[n_r][c] = cuke
  return moves, new_grid

def step(grid):
  east_moves, east_grid = step_east(grid)
  south_moves, south_grid = step_south(east_grid)

  return east_moves + south_moves, south_grid

def show(grid):
  for row in grid:
    logging.debug("".join(row))

move_num = 0

logging.debug("Initial state:")
show(my_input)

while True:
  move_num += 1
  moves, my_input = step(my_input)
  show(my_input)
  logging.info(f"Move {move_num} resulted in {moves} moves.")
  if moves == 0: # or move_num > 10:
    break

logging.info(f"No more moves after {move_num} moves.")
