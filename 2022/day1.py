from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2022, day=1)

lines = p.input_data.splitlines()

cal_counts = []
current_cal_count = 0
for line in lines:
  if line == '':
    cal_counts.append(current_cal_count)
    current_cal_count = 0
    continue

  n = int(line)
  current_cal_count += n

p.answer_a = max(cal_counts)

p.answer_b = sum(sorted(cal_counts)[-3:])
