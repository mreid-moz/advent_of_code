from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

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

start = (0,0)

positions = set()
head = start
tail = start
positions.add(start)

for line in lines:
  direction, distance = line.split(' ')
  distance = int(distance)
  logging.debug(f"Moving Head {direction} {distance} from {head}")
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

  hx, hy = head
  tx, ty = tail
  for i in range(distance):
    hx += dx
    hy += dy
    logging.debug(f"Moved head to {hx},{hy}")
    head = (hx, hy)
    if abs(hx - tx) > 1 or abs(hy - ty) > 1:
      logging.debug(f"Moving tail from {tx},{ty} to catch up to {hx},{hy}")
      # in a line, move ahead
      if hx == tx:
        ty += dy
      elif hy == ty:
        tx += dx
      elif abs(hx - tx) > abs(hy - ty):
        tx += dx
        ty = hy
      elif abs(hx - tx) < abs(hy - ty):
        ty += dy
        tx = hx
      else:
        logging.warn("Not sure how this is possible")
      logging.debug(f"Tail moved to {tx},{ty} to catch up to {hx},{hy}")
      tail = (tx,ty)
      positions.add(tail)

logging.info(f"Found {len(positions)} positions")
p.answer_a = len(positions)
