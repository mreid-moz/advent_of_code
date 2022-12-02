from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2018, day=6)

lines = p.input_data.splitlines()

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

print(f"Min x: {min_x}, max x: {max_x}, min_y = {min_y}, max_y = {max_y}")
# p.answer_a = 10

