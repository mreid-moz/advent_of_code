from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.INFO)

puzz = Puzzle(year=2022, day=15)

pattern = re.compile(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")

TEST = True

if TEST:
  lines = [
    "Sensor at x=2, y=18: closest beacon is at x=-2, y=15",
    "Sensor at x=9, y=16: closest beacon is at x=10, y=16",
    "Sensor at x=13, y=2: closest beacon is at x=15, y=3",
    "Sensor at x=12, y=14: closest beacon is at x=10, y=16",
    "Sensor at x=10, y=20: closest beacon is at x=10, y=16",
    "Sensor at x=14, y=17: closest beacon is at x=10, y=16",
    "Sensor at x=8, y=7: closest beacon is at x=2, y=10",
    "Sensor at x=2, y=0: closest beacon is at x=2, y=10",
    "Sensor at x=0, y=11: closest beacon is at x=2, y=10",
    "Sensor at x=20, y=14: closest beacon is at x=25, y=17",
    "Sensor at x=17, y=20: closest beacon is at x=21, y=22",
    "Sensor at x=16, y=7: closest beacon is at x=15, y=3",
    "Sensor at x=14, y=3: closest beacon is at x=15, y=3",
    "Sensor at x=20, y=1: closest beacon is at x=15, y=3",
  ]
else:
  lines = puzz.input_data.splitlines()

min_x = None
min_y = None
max_x = None
max_y = None

cave = {}
sensors = {}
beacons = set()
for line in lines:
  m = pattern.match(line)
  if not m:
    logging.warning(f"unexpected line: {line}")
    break
  sx = int(m.group(1))
  sy = int(m.group(2))
  bx = int(m.group(3))
  by = int(m.group(4))

  if min_x is None:
    min_x, min_y, max_x, max_y = sx, sy, sx, sy

  min_x = min(sx, bx, min_x)
  min_y = min(sy, by, min_y)
  max_x = max(sx, bx, max_x)
  max_y = max(sy, by, max_y)
  logging.debug(f"Sensor at {sx},{sy} sees beacon at {bx},{by}")
  sensors[(sx,sy)] = (bx,by)
  beacons.add((bx, by))
  cave[(sx,sy)] = 'S'
  cave[(bx,by)] = 'B'

if TEST:
  target_line = 10
else:
  target_line = 2000000

def mark_sensor_area(cave, sx, sy, bx, by):
  logging.debug(f"filling area around {sx},{sy} with beacon at {bx},{by}")
  cave[(sx, sy)] = 'S'
  cave[(bx, by)] = 'B'
  distance = abs(sx - bx) + abs(sy - by)
  for yd in range(distance+1):
    logging.debug(f"Filling row {sy-yd} and {sy+yd}")
    for y in [sy + yd, sy - yd]:
      for x in range(sx - distance + yd, sx + distance - yd + 1):
        logging.debug(f"Filling {x},{y}")
        if (x, y) not in cave:
          cave[x, y] = '#'

def print_cave(cave):
  print(f"x: {min_x} to {max_x}")
  print(f"y: {min_y} to {max_y}")
  for y in range(min_y, max_y + 1):
    for x in range(min_x, max_x + 1):
      v = '.'
      if (x, y) in cave:
        v = cave[(x,y)]
      print(v, end='')
    print('')

logging.debug(f"min x: {min_x}, max x: {max_x}; min y: {min_y}, max y: {max_y}")

# print_cave(cave)

logging.debug(f"Found {len(sensors)} sensors.")

for (sx, sy), (bx, by) in sensors.items():
  logging.info(f"filling cave based on sensor at {sx},{sy}")
  mark_sensor_area(cave, sx, sy, bx, by)

# for row_delta in range(((max_x - min_x) // 2) + 2):
#   # fill target + / - row_delta
#   x_start = min_x + row_delta
#   x_end = max_x - row_delta
#   if x_end < x_start:
#     continue

#   for y in [target_line - row_delta, target_line + row_delta]:
#     logging.debug(f"searching row {y} from x {x_start} to {x_end}")
#     # Find all sensors in that range
#     for x in range(x_start, x_end + 1):
#       if (x, y) in sensors:
#         bx, by = sensors[(x,y)]
#         logging.debug(f"Found a sensor at {x},{y} with beacon at {bx},{by}")
#         # Fill the map from each sensor
#         mark_sensor_area(cave, x, y, bx, by)
#         # print_cave(cave)

no_beacon_count = 0
for (kx, ky), v in cave.items():
  if ky == target_line:
    if v == '#':
      no_beacon_count += 1

logging.info(f"Found {no_beacon_count} positions that cannot have a beacon in row {target_line}")
if not TEST:
  puzz.answer_a = no_beacon_count
