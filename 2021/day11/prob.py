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

def print(grid):
  for row in grid:
    logging.debug("".join([str(n) for n in row]))

def safe_increment(grid, r, c):
  if r < 0 or c < 0:
    return None
  if r >= len(grid) or c >= len(grid[0]):
    return None
  grid[r][c] += 1
  return grid[r][c]

def step(grid):
  ten_count = []
  for r in range(len(grid)):
    for c in range(len(grid[0])):
      grid[r][c] += 1
      if grid[r][c] == 10:
        ten_count.append((r, c))

  while len(ten_count) > 0:
    r, c = ten_count.pop()
    for i in [-1,0,1]:
      for j in [-1,0,1]:
        if i == 0 and j == 0:
          continue
        v = safe_increment(grid, r+i, c+j)
        if v and v == 10:
          ten_count.append((r+i, c+j))

  flash_count = 0
  for r in range(len(grid)):
    for c in range(len(grid[0])):
      if grid[r][c] > 9:
        flash_count += 1
        grid[r][c] = 0
  return flash_count

octo = copy.deepcopy(my_input)
flashes = 0
for i in range(100):
  flashes += step(octo)
  logging.debug("After {} steps, we saw {} flashes.".format(i+1, flashes))
  print(octo)

logging.info("After {} steps, total flashes: {}".format(i+1, flashes))

octo = copy.deepcopy(my_input)
steps = 0
while True:
  current_flashes = step(octo)
  steps += 1
  if current_flashes == 100:
    logging.info("After {} steps, we saw everything flash".format(steps))
    break



