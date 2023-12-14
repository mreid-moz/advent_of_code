from aocd.models import Puzzle
from collections import defaultdict
from utils import rows_to_cols
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2023, day=13)


TEST = False
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

def get_reflection(pattern, include_all=False):
    refs = []
    for i, line in enumerate(pattern):
        before_count = i + 1
        after_count = len(pattern) - i - 1

        if before_count < 1 or after_count < 1:
            continue

        reflection_count = min(before_count, after_count)
        # logging.debug("A reflection at {i} in pattern {j} will be {reflection_count} lines long".format(**locals()))
        all_match = True
        for r in range(reflection_count):
            if pattern[i - r] != pattern[i + r + 1]:
                all_match = False
                break
        if all_match:
            # logging.info("Found a reflection after {}: all {} lines matched".format(i+1, reflection_count))
            if include_all:
                refs.append(i + 1)
            else:
                return i + 1
    if include_all:
        return refs
    return None


def get_either_reflection(pattern, include_all=False):
    h = get_reflection(pattern, include_all)
    if not include_all and h is not None:
        return ('h', h)

    t = rows_to_cols(pattern)
    v = get_reflection(t, include_all)

    if include_all:
        return [('h', hh) for hh in h] + [('v', vv) for vv in v]
    else:
        return ('v', v)

def flip(c):
    if c == '.':
        return '#'
    return '.'

def smudge(pattern, x, y):
    smudged = []
    for yi, line in enumerate(pattern):
        if yi == y:
            new_line = line[0:x] + flip(line[x]) + line[x+1:]
            smudged.append(new_line)
        else:
            smudged.append(line)
    return smudged

def tally(verticals, horizontals):
    return sum(verticals) + sum([h*100 for h in horizontals])

def find_new_reflection(pattern, old_dir, old_location):
    # try each smudge to find a new one.
    for y in range(len(pattern)):
        for x in range(len(pattern[0])):
            # logging.debug("Smudging {},{}".format(x, y))
            smudged = smudge(pattern, x, y)
            refs = get_either_reflection(smudged, include_all=True)
            # logging.debug("refs={}".format(refs))
            for (dn, rn) in refs:
                # logging.debug("Found a potential {} reflection at {}".format(dn, rn))
                if rn is not None and (old_dir, old_location) != (dn, rn):
                    # logging.debug("Found a new {} reflection at {}".format(dn, rn))
                    return (dn, rn, x, y)
    return ('h', None, None, None)

# logging.info("Found {} patterns".format(len(patterns)))
# vertical_reflections = []
# horizontal_reflections = []
# for j, pattern in enumerate(patterns):
#     logging.info("Pattern {}:".format(j))
#     d, r = get_either_reflection(pattern)
#     if r is None:
#         logging.warning("Found neither type of reflection in pattern {}".format(j))
#     else:
#         if d == 'h':
#             horizontal_reflections.append(r)
#         else:
#             vertical_reflections.append(r)

# total = tally(vertical_reflections, horizontal_reflections)
# logging.info("Total: {}".format(total))

# if not TEST:
#     p.answer_a = total

# test = [
#     '...',
#     '###',
#     '...',
# ]

# for y in range(len(test)):
#     for x in range(len(test[0])):
#         smudged = smudge(test, x, y)
#         for line in smudged:
#             print(line)
#         print('')

# part 2
vertical_reflections = []
horizontal_reflections = []
for j, pattern in enumerate(patterns):
    logging.info("Pattern {}:".format(j))
    d, r = get_either_reflection(pattern)
    if r is None:
        logging.warning("Found neither type of reflection in pattern {}".format(j))

    logging.debug("Old reflection: {} at {}".format(d, r))

    # try each smudge to find a new one.
    dn, rn, x, y = find_new_reflection(pattern, d, r)
    if rn is not None:
        logging.debug("Found new reflection with smudge at {},{}".format(x, y))
        if dn == 'h':
            horizontal_reflections.append(rn)
        else:
            vertical_reflections.append(rn)

total = tally(vertical_reflections, horizontal_reflections)
logging.info("Total: {}".format(total))

if not TEST:
    p.answer_b = total

# test = [
# '##....##.#.',
# '##.##.#..#.',
# '..####....#',
# '#######..##',
# '##..#......',
# '...##......',
# '###....##..',
# '..#.#..##..',
# '...#.#....#',
# '..##.......',
# '..##.#.##.#',
# '##...##..##',
# '######.##.#',
# '###...#..#.',
# '...###....#',
# '..##.......',
# '###.##....#',
# ]

# d, r = get_either_reflection(test)
# logging.info("Reflection {} at {}".format(d, r))

# dn, rn, x, y = find_new_reflection(test, d, r)
# logging.info("new reflection: {dn} at {rn} with smudge at {x},{y}".format(**locals()))
