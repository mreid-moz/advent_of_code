import logging
import copy
import re
import sys
from collections import defaultdict

logging.basicConfig(level=logging.INFO)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [[int(x) for x in list(l.strip())] for l in fin.readlines()]

rows = len(my_input)
cols = len(my_input[0])

min_score = None
min_score_path = None
total_path_count = 0

def find_path(grid, x, y, current_path):
  global min_score, min_score_path, total_path_count # :(
  if x == cols - 1 and y == rows - 1:
    score = sum([grid[y][x] for x,y in current_path]) + grid[y][x]
    logging.debug("Found a path with score {}".format(score))
    total_path_count += 1
    if min_score is None or score < min_score:
      logging.info("Total: {}. Found a new min path to ({},{}) with score {}".format(total_path_count, x, y, score))
      min_score = score
      min_score_path = current_path
    return

  for xd in [-1,1]:
    for yd in [-1,1]:
      next_x = x + xd
      next_y = y + yd
      if (next_x, next_y) in current_path:
        continue
      if next_x >= rows or next_x < 0:
        continue
      if next_y >= cols or next_y < 0:
        continue
      find_path(grid, next_x, next_y, current_path + [(x, y)])

find_path(my_input, 0, 0, [])

logging.info("Found a path with min score of {}: {}".format(min_score, min_score_path))