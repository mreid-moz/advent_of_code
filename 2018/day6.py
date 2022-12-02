from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.INFO)

puzz = Puzzle(year=2018, day=6)

lines = puzz.input_data.splitlines()

class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __str__(self):
    return f"{self.x}, {self.y}"

def make_point(line):
  # 123, 456
  left, right = line.split(",")
  return Point(int(left.strip()), int(right.strip()))

def distance(p1, p2):
  return abs(p1.x - p2.x) + abs(p1.y - p2.y)

points = [make_point(line) for line in lines]

max_x = points[0].x
min_x = points[0].x
max_y = points[0].y
min_y = points[0].y

for p in points:
  if p.x < min_x:
    min_x = p.x
  if p.x > max_x:
    max_x = p.x
  if p.y < min_y:
    min_y = p.y
  if p.y > max_y:
    max_y = p.y

logging.debug(f"Min x: {min_x}, max x: {max_x}, min_y = {min_y}, max_y = {max_y}")

map = []
for i in range(max_x + 1):
  map.append([(None, 0, 0)] * (max_y + 1))

for xi in range(min_x - 1, max_x):
  for yi in range(min_y - 1, max_y):
    logging.debug(f"checking ({xi},{yi})")
    curr_point, curr_dist, curr_count = map[xi][yi]
    pi = Point(xi, yi)
    for p in points:
      p_dist = distance(p, pi)
      if curr_point is None or p_dist < curr_dist:
        curr_point = p
        curr_dist = p_dist
        curr_count = 1
        map[xi][yi] = (curr_point, curr_dist, curr_count)
      elif p_dist == curr_dist:
        curr_count += 1
        map[xi][yi] = (curr_point, curr_dist, curr_count)

areas = defaultdict(int)
for xi in range(min_x - 1, max_x):
  for yi in range(min_y - 1, max_y):
    curr_point, curr_dist, curr_count = map[xi][yi]
    if curr_count == 1:
      areas[str(curr_point)] += 1

max_area = 0
max_p = None
for pt, area in areas.items():
  if area > max_area:
    max_area = area
    max_p = pt

logging.info(f"largest area was around {max_p} of size {max_area}")

puzz.answer_a = max_area