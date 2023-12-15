from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2023, day=15)

TEST = False
if TEST:
    lines = p.examples[0].input_data.splitlines()
else:
    lines = p.input_data.splitlines()

def hash(s):
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h %= 256
    return h

def focusing_power(m):
    power = 0
    for box_num, lenses in m.items():
        for i, (lens, focal_length) in enumerate(lenses):
            current_power = (box_num + 1) * (i + 1) * focal_length
            logging.info("Power of box {}, item {}, fl {} is {}".format(box_num, i+1, focal_length, current_power))
            power += current_power
    return power



# logging.info("HASH -> {}".format(hash('HASH')))

sum_of_hashes = 0
for line in lines:
    steps = line.split(',')
    for s in steps:
        sum_of_hashes += hash(s)

logging.info("Sum of step hashes: {}".format(sum_of_hashes))
if not TEST:
    p.answer_a = sum_of_hashes

boxes = defaultdict(list)
for line in lines:
    steps = line.split(',')
    for s in steps:
        label = None
        action = 'add'
        slot = None
        if s[-1] == '-':
            action = 'remove'
            label = s[:-1]
        else:
            label, slot_str = s.split('=')
            slot = int(slot_str)
        label_hash = hash(label)
        logging.debug("hash({}) = {}, {} it at {}".format(label, label_hash, action, slot))
        if action == 'remove':
            cleaned = [(a, b) for (a, b) in boxes[label_hash] if a != label]
            boxes[label_hash] = cleaned
        else:
            found = False
            fixed = [x for x in boxes[label_hash]]
            for i, (l, s) in enumerate(fixed):
                if l == label:
                    fixed[i] = (l, slot)
                    boxes[label_hash] = fixed
                    found = True
            if not found:
                boxes[label_hash].append((label, slot))
        logging.debug("New keys for {}: {}".format(label_hash, boxes[label_hash]))

total_power = focusing_power(boxes)
logging.info("Focusing power: {}".format(total_power))
if not TEST:
    p.answer_b = total_power
