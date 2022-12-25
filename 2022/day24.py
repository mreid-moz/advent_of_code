from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.INFO)

p = Puzzle(year=2022, day=24)

TEST = True
# TEST = False

if TEST:
  lines = [
    "#.######",
    "#>>.<^<#",
    "#.<..<<#",
    "#>v.><>#",
    "#<^v^^>#",
    "######.#",
  ]
else:
  lines = p.input_data.splitlines()

def print_grid(g):
  print('#.', end='')
  print('#' * len(g[0]))
  for row in g:
    print('#', end='')
    for c, blizz in enumerate(row):
      v = ''
      if len(blizz) == 0:
        v = '.'
      elif len(blizz) == 1:
        v = blizz[0]
      else:
        v = str(len(blizz))
      print(v, end='')
    print('#')
  print('#' * len(g[0]), end='')
  print('.#')


def make_grid(rows, cols, initializer=None):
  g = []
  for r in range(rows):
    g.append([])
    for c in range(cols):
      g[r].append([])
      if initializer is not None:
        g[r][c] = initializer()
  return g

def evolve(g):
  new_grid = make_grid(len(g), len(g[0]), list)
  for row, line in enumerate(g):
    for col, blizz in enumerate(line):
      # new_grid[row][col] = []
      for b in blizz:
        new_row = row
        new_col = col
        if b == '>':
          if col + 1 >= len(line):
            new_col = 0
          else:
            new_col = col+1
        elif b == '<':
          if col - 1 < 0:
            new_col = len(line) - 1
          else:
            new_col = col - 1
        elif b == '^':
          if row - 1 < 0:
            new_row = len(g) - 1
          else:
            new_row = row - 1
        elif b == 'v':
          if row + 1 >= len(g):
            new_row = 0
          else:
            new_row = row + 1
        else:
          logging.warning(f"Unexpected blizzard direction: {b}")
        logging.debug(f"Moving {b} from {row},{col} to {new_row},{new_col}")
        new_grid[new_row][new_col].append(b)
  return new_grid

def get_available_spaces(g, current_position):
  spaces = set()
  spaces.add(initial_position)

# sort by manhattan distance
def sort_path(path):
  r,c = path[-1]
  return abs(len(grid) - r) + abs(len(grid[0]) - c)

grid = []

initial_position = (0,-1)
goal_position = (len(lines[-1]) - 3, len(lines) - 2)

for i, line in enumerate(lines[1:-1]):
  grid.append([])
  for blizz in line[1:-1]:
    if blizz == '.':
      grid[i].append([])
    else:
      grid[i].append([blizz])

logging.debug("Initial grid:")
print_grid(grid)

def seek(grid, start_pos, goal_pos):
  goal_row, goal_col = goal_pos
  all_paths = [[start_pos]]
  shortest_path = None
  i = 0
  while shortest_path is None:
    i += 1
    logging.info(f"Minute {i}:")
    grid = evolve(grid)
    if TEST:
      print_grid(grid)
    new_paths = []
    # Keep just one path per distinct endpoint - any of them will do.
    ends = set()
    logging.info(f"Looking at {len(all_paths)} paths of length {len(all_paths[0])}")
    for path in all_paths:
      logging.debug(f"Looking at path {path}")
      cr, cc = path[-1]
      for nr, nc in [(cr, cc), (cr - 1, cc), (cr + 1, cc), (cr, cc - 1), (cr, cc + 1)]:
        if nr == goal_row and nc == goal_col:
          # done!
          shortest_path = len(path)
          logging.info(f"Shortest path: {shortest_path} -> {path}")
          return shortest_path
        if nr < 0 or nc < 0 or nr >= len(grid) or nc >= len(grid[0]):
          continue
        if len(grid[nr][nc]) == 0:
          logging.debug(f"found a potential step from {cr},{cc} -> {nr},{nc}")
          if (nr,nc) in ends:
            logging.debug(f"Already have a path of length {len(path) + 1} ending at ({nr},{nc}). Skipping path")
          else:
            logging.debug(f"Keeping a path of length {len(path) + 1} ending at ({nr},{nc}). Keeping path")
            ends.add((nr,nc))
            new_paths.append(path + [(nr, nc)])
      if shortest_path is not None:
        break
    if shortest_path is not None:
      break

    if len(new_paths) == 0:
      logging.info("Ran out of paths :(")
      return None

    all_paths = new_paths
    logging.info(f"Closest of {len(all_paths)}: {sort_path(all_paths[0])}, furthest: {sort_path(all_paths[-1])}")
  return shortest_path

shortest_path = seek(grid, initial_position, goal_position)
logging.info(f"Found a short path of {shortest_path}")
# p.answer_a = 10

# logging.info("turning around...")
# path_back = seek(grid, goal_position, initial_position)
# logging.info(f"Found shortest path back: {path_back}")

# logging.info("turning around...")
# path_forth = seek(grid, initial_position, goal_position)
# logging.info(f"Found shortest path forth: {path_forth}")

# total_time = shortest_path + path_back + path_forth
# logging.info(f"Total time: {total_time}")

