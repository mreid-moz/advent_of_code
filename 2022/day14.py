from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

puzz = Puzzle(year=2022, day=14)

lines = puzz.input_data.splitlines()
# lines = [
#   "498,4 -> 498,6 -> 496,6",
#   "503,4 -> 502,4 -> 502,9 -> 494,9",
# ]

cave = {}
source = (500,0)
min_x = 500
min_y = 0
max_x = 500
max_y = 0

for line in lines:
  points = line.split(" -> ")
  prev_x = 0
  prev_y = 0
  for i, p in enumerate(points):
    logging.debug(f"Point: {p}")
    x, y = [int(n) for n in p.split(",")]
    if x < min_x:
      min_x = x
    if y < min_y:
      min_y = y
    if x > max_x:
      max_x = x
    if y > max_y:
      max_y = y
    logging.debug(f"Found a point {x, y}")
    if i > 0:
      for xi in range(min(prev_x, x), max(prev_x, x) + 1):
        for yi in range(min(prev_y, y), max(prev_y, y) + 1):
          logging.debug(f"Rock at {xi, yi}")
          cave[(xi, yi)] = '#'
    prev_x, prev_y = x, y

for x in range(min_x, max_x + 1):
  for y in range(min_y, max_y + 1):
    if (x, y) not in cave:
      cave[(x,y)] = ' '

def print_cave(cave):
  print(f"x: {min_x} to {max_x}")
  print(f"y: {min_y} to {max_y}")
  for y in range(min_y, max_y + 1):
    for x in range(min_x, max_x + 1):
      v = ' '
      if (x, y) in cave:
        v = cave[(x,y)]
      print(v, end='')
    print('')

print_cave(cave)

PART_ONE = False

if not PART_ONE:
  # expand the cave, add the floor.
  for x in range(min_x - 500, max_x + 501):
    cave[(x, max_y+1)] = ' '
    cave[(x, max_y+2)] = '#'

  max_y += 2
  min_x -= 500
  max_x += 500

  for x in range(min_x, max_x+1):
    for y in range(min_y, max_y+1):
      if (x, y) not in cave:
        cave[(x, y)] = ' '

done = False
fell = False
while not done:
  fell = False
  sand_x, sand_y = source
  blocked_below = False
  while not blocked_below:
    by = sand_y + 1
    # move straight down if possible
    bx = sand_x
    if (bx, by) not in cave:
      logging.debug(f"sand fell off the map to the bottom at {bx},{by}")
      fell = True
      done = True
      break
    elif cave[(bx, by)] == ' ':
      sand_x, sand_y = bx, by
      continue
    else:
      # straight down is blocked, try left
      bx = sand_x - 1
      if (bx, by) not in cave:
        logging.debug(f"sand fell off the map to the left at {bx},{by}")
        fell = True
        done = True
        break
      elif cave[(bx,by)] == ' ':
        sand_x, sand_y = bx, by
      else:
        # left is blocked, try right
        bx = sand_x + 1
        if (bx, by) not in cave:
          logging.debug(f"sand fell off the map to the right at {bx},{by}")
          fell = True
          done = True
          break
        elif cave[(bx,by)] == ' ':
          sand_x, sand_y = bx, by
        else:
          blocked_below = True
          break

  if (sand_x, sand_y) == source:
    logging.debug("sand couldn't move, all done")
    cave[(sand_x,sand_y)] = 'o'
    done = True
  elif not fell:
    cave[(sand_x,sand_y)] = 'o'

print_cave(cave)

sand_count = 0
for k, v in cave.items():
  if v == 'o':
    sand_count += 1

logging.info(f"Found {sand_count} sand")

if PART_ONE:
  puzz.answer_a = sand_count
else:
  puzz.answer_b = sand_count
