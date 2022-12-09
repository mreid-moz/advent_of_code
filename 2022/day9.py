from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.INFO)

p = Puzzle(year=2022, day=9)

lines = p.input_data.splitlines()
# lines = [
#   "R 4",
#   "U 4",
#   "L 3",
#   "D 1",
#   "R 4",
#   "D 1",
#   "L 5",
#   "R 2",
# ]

# lines = [
#   "R 5",
#   "U 8",
#   "L 8",
#   "D 3",
#   "R 17",
#   "D 10",
#   "L 25",
#   "U 20",
# ]

# part a: set to 1
num_knots = 10
knots = [(0,0)] * num_knots

positions = set()
positions.add(knots[0])

for line in lines:
  direction, distance = line.split(' ')
  distance = int(distance)
  logging.debug(f"Moving Head {direction} {distance} from {knots[0]}")
  dx = 0
  dy = 0
  if direction == 'U':
    dy = 1
  elif direction == 'D':
    dy = -1
  elif direction == 'L':
    dx = -1
  elif direction == 'R':
    dx = 1
  else:
    logging.warn(f"Unexpected direction {direction}")

  for i in range(distance):
    hx, hy = knots[0]
    hx += dx
    hy += dy
    logging.debug(f"Moved head to {hx},{hy}")
    knots[0] = (hx, hy)

    for i in range(len(knots) - 1):
      hx, hy = knots[i]
      tx, ty = knots[i + 1]
      knot_dx = hx - tx
      knot_dy = hy - ty
      if abs(knot_dx) > 1 or abs(knot_dy) > 1:
        logging.debug(f"Moving knot {i+1} from {tx},{ty} to catch up to {hx},{hy}")
        # in a line, move ahead
        if hx == tx:
          ty += knot_dy // 2
        elif hy == ty:
          tx += knot_dx // 2
        elif abs(knot_dx) > abs(knot_dy): # Diagonal
          tx += knot_dx // 2
          ty = hy
        elif abs(knot_dx) < abs(knot_dy):
          ty += knot_dy // 2
          tx = hx
        elif abs(knot_dx) == abs(knot_dy):
          # 2 away in both dirs
          tx += knot_dx // 2
          ty += knot_dy // 2
        else:
          logging.warning(f"Not sure how this is possible: dx={knot_dx}, dy={knot_dy}")
        logging.debug(f"Knot moved to {tx},{ty} to catch up to {hx},{hy}")
        knots[i+1] = (tx,ty)
    # keep track of positions of the last knot only
    positions.add(knots[-1])

logging.info(f"Found {len(positions)} positions")
#p.answer_a = len(positions)
p.answer_b = len(positions)
