from aocd.models import Puzzle
from collections import defaultdict
from functools import cmp_to_key
import logging
import re
import sys

logging.basicConfig(level=logging.INFO)

p = Puzzle(year=2024, day=5)

TEST = False
if TEST:
    lines = p.examples[0].input_data.splitlines()
else:
    lines = p.input_data.splitlines()

rules = []
updates = []

update_mode = False

for line in lines:
    if line == '':
        update_mode = True
        continue

    if update_mode:
        updates.append([int(s) for s in line.split(',')])
    else:
        rules.append([int(s) for s in line.split('|')])

logging.debug(f"Found {len(rules)} rules and {len(updates)} updates")

def middle(list):
    return list[len(list) // 2]

def is_ordered(update, rules):
    for i in range(1, len(update)):
        logging.debug(f"Looking at {i}")
        for b in range(i):
            logging.debug(f"Comparing before: {i} and {b}")
            if [update[i], update[b]] in rules:
                logging.info(f"Update {update} no good because of rule {update[i]}|{update[b]}")
                return False
        for a in range(i+1, len(update)):
            logging.debug(f"Comparing after: {i} and {a}")
            if [update[a], update[i]] in rules:
                logging.info(f"Update {update} no good because of rule {update[a]}|{update[i]}")
                return False
    return True

def reorder(update, rules):
    def compare(a, b):
        if [a, b] in rules:
            return -1
        if [b, a] in rules:
            return 1
        return 0
    return sorted(update, key=cmp_to_key(compare))

total = 0
not_ordered = []
for update in updates:
    if is_ordered(update, rules):
        total += middle(update)
    else:
        not_ordered.append(update)

logging.info(f"Sum: {total}")

bad_total = 0
for bad in not_ordered:
    reordered = reorder(bad, rules)
    bad_total += middle(reordered)

logging.info(f"Sum after reordering: {bad_total}")

if not TEST:
    p.answer_a = total
    p.answer_b = bad_total
