from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.INFO)

puzz = Puzzle(year=2022, day=15)

pattern = re.compile(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")

TEST = False

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
  target_y_max = 20
else:
  lines = puzz.input_data.splitlines()
  target_y_max = 4000000

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

def mark_sensor_area(cave, sx, sy, bx, by, target_line):
  #logging.debug(f"filling area around {sx},{sy} with beacon at {bx},{by}")
  distance = abs(sx - bx) + abs(sy - by)
  target_line_distance = abs(sy - target_line)
  if target_line_distance > distance:
    return

  y = target_line
  #logging.debug(f"Filling row {y}")
  for x in range(sx - distance + target_line_distance, sx + distance - target_line_distance + 1):
    #logging.debug(f"Filling {x},{y}")
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

#print_cave(cave)
#
#for (sx, sy), (bx, by) in sensors.items():
#  logging.debug(f"filling area around {sx},{sy} with beacon at {bx},{by}")
#  distance = abs(sx - bx) + abs(sy - by)
#  for y in range(sy - distance, sy + distance + 1):
#    mark_sensor_area(cave, sx, sy, bx, by, y)
#
#print_cave(cave)

logging.debug(f"Found {len(sensors)} sensors.")

def subtract(start, end, sub_start, sub_end):
  # logging.info(f"subtracting {sub_start}-{sub_end} from {start}-{end}")
  subtracted = []
  if sub_start < start and sub_end > end:
    # thing to be subtracted covers the thing
    # logging.debug("total overlap")
    pass
  elif sub_start > end or sub_end < start:
    # doesn't overlap at all
    # logging.debug("no overlap")
    subtracted.append((start, end))
  elif sub_start > start and sub_end < end:
    # it's in the middle
    # logging.debug("middle")
    subtracted.append((start, sub_start - 1))
    subtracted.append((sub_end + 1, end))
  elif sub_start < end and sub_end >= end:
    # it overlaps on the high end
    # logging.debug("high end")
    subtracted.append((start, sub_start - 1))
  elif sub_start <= start and sub_end > start:
    # it overlaps on the low end
    # logging.debug("low end")
    subtracted.append((sub_end + 1, end))
  # logging.debug(f"Subtracted: {subtracted}")
  return subtracted

def get_empty_spaces(sensors, target_line, xmin=0, xmax=4000000):
  filled_spaces = []
  for (sx, sy), (bx, by) in sensors.items():
    logging.debug(f"filling area around {sx},{sy} with beacon at {bx},{by}")
    distance = abs(sx - bx) + abs(sy - by)
    target_line_distance = abs(sy - target_line)
    if target_line_distance > distance:
      continue

    a = sx - distance + target_line_distance
    b = sx + distance - target_line_distance
    logging.debug(f"Adding {min(a,b)},{max(a,b)} to line {target_line}")
    filled_spaces.append((min(a,b), max(a,b)))
  logging.debug(f"filled spaces: {filled_spaces}")

  empty_spaces = [(xmin, xmax)]
  for fs_start, fs_end in filled_spaces:
    new_empty_spaces = []
    for es_start, es_end in empty_spaces:
      new_empty_spaces += subtract(es_start, es_end, fs_start, fs_end)
    empty_spaces = new_empty_spaces
  return empty_spaces

def length_space(space):
  l = 0
  for ss, se in space:
    l += se - ss + 1
  return l

target_x = None
target_y = None
for i in range(target_y_max):
  espace = get_empty_spaces(sensors, i, 0, target_y_max)
  if i % 10000 == 0:
    logging.info(f"line {i}: espace {espace}")
  lspace = length_space(espace)
  #logging.info(f"Found a line with {lspace} space: {i}")
  if lspace == 1:
    target_x = espace[0][0]
    target_y = i
    #logging.info(f"x was {target_x}, y was {target_y}")
    break

if target_x is not None:
  logging.info(f"tuning freq: {target_x * 4000000 + target_y}")

