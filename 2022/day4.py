from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2022, day=4)

lines = p.input_data.splitlines()

pattern = re.compile(r"(\d+)-(\d+),(\d+)-(\d+)")

contain_count = 0
overlap_count = 0
for line in lines:
  m = pattern.match(line)
  if m is None:
    logging.warn(f"Bad input: {line}")
    break
  ll = int(m.group(1))
  lh = int(m.group(2))
  rl = int(m.group(3))
  rh = int(m.group(4))

  # left contains right:
  if ll <= rl and lh >= rh:
    contain_count += 1
  elif rl <= ll and rh >= lh: # right contains left
    contain_count += 1

  # Overlaps:
  if ll <= rl and lh >= rl:
    overlap_count += 1
  elif rl <= ll and rh >= ll:
    overlap_count += 1

logging.info(f"Found {contain_count} contained")
p.answer_a = contain_count

logging.info(f"Found {overlap_count} overlapping")
p.answer_b = overlap_count
