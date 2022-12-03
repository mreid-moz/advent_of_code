from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2022, day=3)

lines = p.input_data.splitlines()

def priority(letter):
  # ord('a') = 97
  # ord('A') = 65
  o = ord(letter)
  if o < 97:
    # uppercase
    return o - 38
  return o - 96

total = 0
for line in lines:
  middle = int(len(line)/2)
  left = line[:middle]
  right = line[middle:]
  common = set(left) & set(right)
  total += priority(common.pop())

p.answer_a = total

total = 0
logging.debug(f"Total lines: {len(lines)}")
for i in range(0, len(lines), 3):
  logging.debug(i)
  one = set(lines[i])
  two = one & set(lines[i+1])
  three = two & set(lines[i+2])
  total += priority(three.pop())

p.answer_b = total