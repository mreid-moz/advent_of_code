from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.INFO)

p = Puzzle(year=2022, day=23)

TEST = True
TEST = False

if TEST:
  lines = [
    "....#..",
    "..###.#",
    "#...#.#",
    ".#...##",
    "#.###..",
    "##.#.##",
    ".#..#..",
  ]
  # lines = [
  #   ".....",
  #   "..##.",
  #   "..#..",
  #   ".....",
  #   "..##.",
  #   ".....",
  # ]
else:
  lines = p.input_data.splitlines()

ground = {}

min_row = None
min_col = None
max_row = None
max_col = None

for row, line in enumerate(lines):
  for col, val in enumerate(line):
    if val == '#':
      ground[(row,col)] = val
      if min_row is None or row < min_row:
        min_row = row
      if min_col is None or col < min_col:
        min_col = col
      if max_row is None or row > max_row:
        max_row = row
      if max_col is None or col > max_col:
        max_col = col

logging.info(f"Bounding rectangle is ({min_row},{min_col}) to ({max_row},{max_col})")

directions = ['north','south','west','east']

def find_moves(ground, diridx):
  moves = []
  move_counter = defaultdict(int)
  for (row,col), v in ground.items():
    free = {}
    free['nw'] = (row-1, col-1) not in ground
    free['n']  = (row-1, col)   not in ground
    free['ne'] = (row-1, col+1) not in ground
    free['sw'] = (row+1, col-1) not in ground
    free['s']  = (row+1, col)   not in ground
    free['se'] = (row+1, col+1) not in ground
    free['w']  = (row,   col-1) not in ground
    free['e']  = (row,   col+1) not in ground

    if (free['nw'] and free['n'] and free['ne'] and
        free['sw'] and free['s'] and free['se'] and
        free['w'] and free['e']):
      continue

    nr, nc = row, col

    for di in range(len(directions)):
      d = directions[(diridx + di) % len(directions)]
      if d == 'north':
        if free['nw'] and free['n'] and free['ne']:
          nr, nc = row-1, col
          logging.debug(f"Can move {row},{col} north to {nr},{nc}")
          break
        #else:
        #  logging.debug("Can't move north")
      if d == 'south':
        if free['sw'] and free['s'] and free['se']:
          nr, nc = row+1, col
          logging.debug(f"Can move {row},{col} south to {nr},{nc}")
          break
        #else:
        #  logging.debug("Can't move south")
      if d == 'west':
        if free['nw'] and free['w'] and free['sw']:
          nr, nc = row, col-1
          logging.debug(f"Can move {row},{col} west to {nr},{nc}")
          break
        #else:
        #  logging.debug("Can't move west")
      if d == 'east':
        if free['ne'] and free['e'] and free['se']:
          nr, nc = row, col+1
          logging.debug(f"Can move {row},{col} east to {nr},{nc}")
          break
        #else:
        #  logging.debug("Can't move east")

    if row != nr or col != nc:
      moves.append((row, col, nr, nc))
      move_counter[(nr,nc)] += 1
  filtered_moves = []
  for r, c, nr, nc in moves:
    if move_counter[(nr,nc)] == 1:
      filtered_moves.append((r,c,nr,nc))
    else:
      logging.debug(f"skipping move {r},{c} -> {nr},{nc} since we saw it {move_counter[(nr,nc)]} times")

  return filtered_moves

def count_empty_tiles(ground, min_row, min_col, max_row, max_col):
  height = max_row - min_row + 1
  width = max_col - min_col + 1
  logging.debug(f"Width: {width} x Height: {height}, number of elves {len(ground)}")
  return width * height - len(ground)


def count_slow(ground):
  min_row = None
  min_col = None
  max_row = None
  max_col = None

  for row, col in ground.keys():
    if min_row is None or row < min_row:
      min_row = row
    if min_col is None or col < min_col:
      min_col = col
    if max_row is None or row > max_row:
      max_row = row
    if max_col is None or col > max_col:
      max_col = col
  height = max_row - min_row + 1
  width = max_col - min_col + 1
  logging.debug(f"Width: {width} x Height: {height}, number of elves {len(ground)}")
  return width * height - len(ground)

def print_tiles(ground, min_row, min_col, max_row, max_col):
  for r in range(min_row, max_row + 1):
    for c in range(min_col, max_col + 1):
      if (r,c) in ground:
        print(ground[(r,c)], end='')
      else:
        print('.', end='')
    print('')

num_rounds = 10
for i in range(num_rounds):
  logging.info(f"Round {i+1}, looking to the {directions[i % len(directions)]} first")
  moves = find_moves(ground, i % len(directions))
  for r, c, nr, nc in moves:
    logging.debug(f"Moving from {r},{c} to {nr},{nc}")
    if nr < min_row:
      min_row = nr
    if nr > max_row:
      max_row = nr
    if nc < min_col:
      min_col = nc
    if nc > max_col:
      max_col = nc

    del ground[(r,c)]
    ground[(nr,nc)] = '#'
  print_tiles(ground, min_row, min_col, max_row, max_col)

# empties = count_empty_tiles(ground, min_row, min_col, max_row, max_col)
empties = count_slow(ground)

logging.info(f"After {num_rounds} rounds, bounding box was ({min_row},{min_col}) to ({max_row},{max_col}) and contained {empties} empty tiles.")

if not TEST:
  p.answer_a = empties

while True:
  i += 1
  if i % 50 == 0:
    logging.info(f"Round {i+1}, looking to the {directions[i % len(directions)]} first")
  moves = find_moves(ground, i % len(directions))
  if not moves:
    logging.info("No moves!")
    break
  for r, c, nr, nc in moves:
    logging.debug(f"Moving from {r},{c} to {nr},{nc}")
    if nr < min_row:
      min_row = nr
    if nr > max_row:
      max_row = nr
    if nc < min_col:
      min_col = nc
    if nc > max_col:
      max_col = nc

    del ground[(r,c)]
    ground[(nr,nc)] = '#'

logging.info(f"No more moves after {i+1} rounds.")
if not TEST:
  p.answer_b = i + 1
