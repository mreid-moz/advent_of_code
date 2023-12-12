from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2023, day=12)

TEST = True
if TEST:
    # lines = p.examples[0].input_data.splitlines()
    lines = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""".splitlines()
else:
    lines = p.input_data.splitlines()

def count_contiguous(springs, lengths, incomplete_ok=False):
    length_idx = 0
    current_length = 0
    contigs = []
    for i, c in enumerate(springs):
        if c == '#':
            current_length += 1
        elif current_length != 0:
            # logging.debug("{} {} at {}: Checking current length {} against lengths[{}]".format(springs, lengths, i, current_length, length_idx))
            if length_idx >= len(lengths):
                return False
            if current_length != lengths[length_idx]:
                return False
            contigs.append(current_length)
            length_idx += 1
            current_length = 0
    if current_length > 0:
        contigs.append(current_length)

    lc = len(contigs)
    ll = len(lengths)
    if lc > ll:
        return False

    for i, c in enumerate(contigs):
        if c != lengths[i]:
            return False
    if incomplete_ok:
        return True
    return len(contigs) == len(lengths)

def count_arrangements(springs, lengths):
    idx = springs.find('?')
    if idx == -1:
        if count_contiguous(springs, lengths):
            # logging.debug("{} {} is a valid arrangement".format(springs, lengths))
            return 1 # valid configuration
        return 0 #invalid configuratioin
    else:
        prefix = springs[0:idx]
        suffix = springs[idx + 1:]

        if count_contiguous(prefix, lengths, incomplete_ok=True):
            # Gotta stop short on early impossible arrangements.
            return count_arrangements(prefix + '#' + suffix, lengths) + count_arrangements(prefix + '.' + suffix, lengths)
        else:
            return 0

# if not p.answered_a:
total_arrangements = 0
for line in lines:
    springs, lengths = line.split(' ')
    lengths = [int(s) for s in lengths.split(',')]
    arrangements = count_arrangements(springs, lengths)
    logging.debug("{} {} -> {} arrangements".format(springs, lengths, arrangements))
    total_arrangements += arrangements

logging.info("Total arrangements: {}".format(total_arrangements))

if not TEST:
    p.answer_a = total_arrangements

# Part 2
total_arrangements = 0
for line in lines:
    springs, lengths = line.split(' ')
    springs = '?'.join([springs] * 5)
    lengths = [int(s) for s in lengths.split(',')]
    lengths = lengths * 5

    logging.debug("Checking {} -> {} {}".format(line, springs, lengths))
    arrangements = count_arrangements(springs, lengths)
    logging.debug("{} -> {} {} -> {} arrangements".format(line, springs, lengths, arrangements))
    total_arrangements += arrangements

logging.info("Total arrangements: {}".format(total_arrangements))

if not TEST:
    p.answer_b = total_arrangements
