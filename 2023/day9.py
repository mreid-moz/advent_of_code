from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2023, day=9)

TEST = False
if TEST:
    lines = p.examples[0].input_data.splitlines()
else:
    lines = p.input_data.splitlines()

def delta_sequence(s):
    new_s = []
    for i in range(len(s) - 1):
        new_s.append(s[i+1] - s[i])
    return new_s

def show(s):
    return ",".join([str(i) for i in s])

def all_zero(s):
    for o in s:
        if o != 0:
            return False
    return True

def get_components(s):
    components = [s[-1]]
    logging.debug("Getting components for {}. First component is {}".format(show(s), components[0]))
    next_seq = delta_sequence(s)
    while not all_zero(next_seq):
        components.append(next_seq[-1])
        logging.debug("Next sequence {}. Components are {}".format(show(next_seq), show(components)))
        next_seq = delta_sequence(next_seq)
    return components

sequences = [[int(s) for s in line.split()] for line in lines]

total = 0
for s in sequences:
    components = get_components(s)
    logging.info("{} -> {}".format(show(s), show(components)))
    total += sum(components)

logging.info("Overall total: {}".format(total))

if not TEST:
    p.answer_a = total

# part 2
total = 0
for s in sequences:
    s.reverse()
    components = get_components(s)
    logging.info("{} -> {} -> {}".format(show(s), show(components), sum(components)))
    total += sum(components)

logging.info("Overall total: {}".format(total))

if not TEST:
    p.answer_b = total
