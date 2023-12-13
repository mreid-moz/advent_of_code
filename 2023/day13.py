from aocd.models import Puzzle
from collections import defaultdict
from utils import rows_to_cols
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2023, day=13)


TEST = True
if TEST:
    lines = p.examples[0].input_data.splitlines()
else:
    lines = p.input_data.splitlines()

patterns = []
current_pattern = []
for line in lines:
    if line == '':
        patterns.append(current_pattern)
        current_pattern = []
    else:
        current_pattern.append(line)
patterns.append(current_pattern)

def get_reflections(pattern):
    vertical_reflections = []
    for i, line in enumerate(pattern):
        before_count = i + 1
        after_count = len(pattern) - i - 1

        if before_count <= 1 or after_count <= 1:
            continue

        reflection_count = min(before_count, after_count)
        # logging.debug("A reflection at {i} in pattern {j} will be {reflection_count} lines long".format(**locals()))
        all_match = True
        for r in range(reflection_count):
            if pattern[i - r] != pattern[i + r + 1]:
                all_match = False
                break
        if all_match:
            logging.info("Found a reflection after {}: all {} lines matched".format(i+1, reflection_count))
            vertical_reflections.append(i+1)
    return vertical_reflections

def tally(verticals, horizontals):
    return sum(verticals) + sum([h*100 for h in horizontals])

logging.info("Found {} patterns".format(len(patterns)))
vertical_reflections = []
horizontal_reflections = []
for j, pattern in enumerate(patterns):
    logging.info("Pattern:")
    for x in pattern:
        print(x)

    logging.debug("Horizontal")
    horizontal_reflections += get_reflections(pattern)

    logging.debug("Rotating...")
    translated = rows_to_cols(pattern)
    for x in translated:
        print(x)

    logging.debug("Vertical")
    vertical_reflections += get_reflections(translated)


total = tally(vertical_reflections, horizontal_reflections)
logging.info("Total: {}".format(total))
if not TEST:
    p.answer_a = total
