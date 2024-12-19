from aocd.models import Puzzle
from collections import defaultdict
from functools import cache
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2024, day=19)

TEST = False
if TEST:
    lines = p.examples[0].input_data.splitlines()
else:
    lines = p.input_data.splitlines()

towels = set(lines[0].split(', '))
patterns = lines[2:]

@cache
def arrangements(pattern):
    if pattern == '':
        return 1
    combos = 0
    for t in towels:
        if pattern.startswith(t):
            combos += arrangements(pattern[len(t):])
    return combos

count = 0
for pattern in patterns:
    if arrangements(pattern) > 0:
        # logging.debug(f"Pattern {pattern} is makeable")
        count += 1

logging.info(f"Of {len(patterns)}, {count} are makeable")
if not TEST:
    p.answer_a = count

count = 0
for pattern in patterns:
    logging.info(f"Trying to make {pattern}...")
    arr = arrangements(pattern)
    logging.info(f"Found {arr} arrangements to make {pattern}")
    count += arr

logging.info(f"We can make the patterns in {count} ways")
if not TEST:
    p.answer_b = count
