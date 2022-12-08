from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2022, day=8)

lines = p.input_data.splitlines()
# lines = [
#   "30373",
#   "25512",
#   "65332",
#   "33549",
#   "35390",
# ]

grid = []
for line in lines:
  grid.append([int(x) for x in list(line)])

def visible(grid, x, y):
  return (visible_north(grid, x, y) or
         visible_south(grid, x, y) or
         visible_east(grid, x, y) or
         visible_west(grid, x, y))

def visible_north(grid, x, y):
  height = grid[x][y]
  for i in range(y):
    if grid[x][i] >= height:
      return False
  return True

def visible_south(grid, x, y):
  height = grid[x][y]
  for i in range(y+1, len(grid[x])):
    if grid[x][i] >= height:
      return False
  return True

def visible_west(grid, x, y):
  height = grid[x][y]
  for i in range(x):
    if grid[i][y] >= height:
      return False
  return True

def visible_east(grid, x, y):
  height = grid[x][y]
  for i in range(x+1, len(grid)):
    if grid[i][y] >= height:
      return False
  return True

visible_trees = 0

for x in range(len(grid)):
  for y in range(len(grid[x])):
    if visible(grid, x, y):
      visible_trees += 1

logging.info(visible_trees)
#p.answer_a = visible_trees

def score(grid, x, y):
  return (score_north(grid, x, y) *
         score_south(grid, x, y) *
         score_east(grid, x, y) *
         score_west(grid, x, y))

def score_north(grid, x, y):
  height = grid[x][y]
  score = 0
  for i in range(y-1, -1, -1):
    logging.debug(f"Looking north from ({x},{y})={height} to ({x},{i})={grid[x][i]}")
    score += 1
    if grid[x][i] >= height:
      break
  logging.debug(f"North score: {score}")
  return score

def score_south(grid, x, y):
  height = grid[x][y]
  score = 0
  for i in range(y+1, len(grid[x])):
    logging.debug(f"Looking south from ({x},{y})={height} to ({x},{i})={grid[x][i]}")
    score += 1
    if grid[x][i] >= height:
      break
  logging.debug(f"South score: {score}")
  return score

def score_west(grid, x, y):
  height = grid[x][y]
  score = 0
  for i in range(x-1, -1, -1):
    logging.debug(f"Looking west from ({x},{y})={height} to ({i},{y})={grid[i][y]}")
    score += 1
    if grid[i][y] >= height:
      break
  logging.debug(f"West score: {score}")
  return score

def score_east(grid, x, y):
  height = grid[x][y]
  score = 0
  for i in range(x+1, len(grid)):
    logging.debug(f"Looking east from ({x},{y})={height} to ({i},{y})={grid[i][y]}")
    score += 1
    if grid[i][y] >= height:
      break
  logging.debug(f"East score: {score}")
  return score

best_score = 0
for x in range(len(grid)):
  for y in range(len(grid[x])):
    s = score(grid, x, y)
    if s > best_score:
      best_score = s

logging.info(best_score)
logging.info(f"Scenic score for (3,2): {score(grid, 3, 2)}")
p.answer_b = best_score
