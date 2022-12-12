from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.INFO)

p = Puzzle(year=2022, day=12)

lines = p.input_data.splitlines()

# lines = [
#   "Sabqponm",
#   "abcryxxl",
#   "accszExk",
#   "acctuvwj",
#   "abdefghi",
# ]

PART_ONE = True

grid = {}
start = None
end = None
for y, line in enumerate(lines):
  for x, c in enumerate(line):
    grid[(x, y)] = ord(c) - ord('a') + 1
    if c == 'S':
      start = (x, y)
      grid[(x, y)] = 0
    elif c == 'E':
      end = (x, y)
      grid[(x, y)] = 27

logging.debug(f"Start: {start} -> End: {end}")

all_paths = []
if PART_ONE:
  all_paths.append([start])
else:
  for k, v in grid.items():
    if v == 0 or v == 1:
      all_paths.append([k])

done = False
shortest_path = -1
while not done:
  new_paths = []
  logging.info(f"Looking at {len(all_paths)} paths of length {len(all_paths[0])}")
  for path in all_paths:
    lx, ly = path[-1]
    lc = grid[(lx, ly)]
    for x, y in [(lx-1, ly), (lx+1, ly), (lx, ly-1), (lx, ly+1)]:
      if (x, y) not in grid or (x, y) in path:
        continue
      c = grid[(x, y)]
      if (c - lc) <= 1:
        new_paths.append(path + [(x, y)])
        logging.debug(f"Found a next step {lx},{ly} ({lc}) -> {x},{y} ({c})")
        if (x, y) == end:
          done = True
          logging.info(f"Found a path to the end: {path}")
          shortest_path = len(path)
          break
      else:
        logging.debug(f"Path was a dead end: {path}")

  # combine paths of the same length that start/end in the same place.
  all_paths = []
  terminals = set()
  for path in new_paths:
    xs,ys = path[0]
    xe,ye = path[-1]
    if (xs,ys,xe,ye) not in terminals:
      all_paths.append(path)
      terminals.add((xs,ys,xe,ye))

logging.info(f"Shortest path: {shortest_path}")

if PART_ONE:
  p.answer_a = shortest_path
else:
  p.answer_b = shortest_path

