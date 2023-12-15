from aocd.models import Puzzle
from collections import defaultdict
from functools import cache
import logging
import re
import sys

logging.basicConfig(level=logging.INFO)

p = Puzzle(year=2023, day=12)

TEST = False
if TEST:
    lines = p.examples[0].input_data.splitlines()
    lines = [
        '???.### 1,1,3',
        '.??..??...?##. 1,1,3',
        '?#?#?#?#?#?#?#? 1,3,1,6',
        '????.#...#... 4,1,1',
        '????.######..#####. 1,6,5',
        '?###???????? 3,2,1',
        # '????#???????#????? 1,8,1,1,1',
        # '??? 1,1',
    ]
else:
    lines = p.input_data.splitlines()

def works(springs, length, offset):
    # logging.debug(' ' * offset + springs[offset:offset+length])
    if '.' in springs[offset:offset+length]:
        # logging.debug("bad 1")
        return False

    # logging.debug("offset+length={}, len(springs)={}".format(length + offset, len(springs)))
    if length + offset < len(springs):
        if springs[offset+length] == '#':
            # logging.debug("bad 2")
            return False
    if offset > 0:
        if springs[offset - 1] == '#':
            # logging.debug("bad 3")
            return False
    # logging.debug("good 1")
    return True

@cache
def count_arrangements(springs, lengths):
    if len(lengths) == 0:
        if '#' not in springs:
            logging.debug("good1")
            return 1
        else:
            logging.debug("bad1")
            return 0

    next_length = lengths[0]
    arrangements = 0
    for i in range(len(springs) - next_length + 1):
        good_or_bad = 'good'
        w = works(springs, next_length, i)
        if not w:
            good_or_bad = 'bad'
        logging.debug('Checking len({}) {}: L {} at O {} "{}" is {}'.format(len(springs), springs, next_length, i, springs[i:i+next_length], good_or_bad))

        if w:
            if i + next_length == len(springs):
                # it's at the end of the string
                logging.debug("Good at the end")
                arrangements += count_arrangements('', lengths[1:])
            else:
                arrangements += count_arrangements(springs[i + next_length + 1:], lengths[1:])
        else:
            # we can't just skip over a spring. If we have see one and it's bad, stop looking.
            if '#' in springs[0:i]:
                break
    return arrangements

total_arrangements = 0
total_orig = 0
for line in lines:
    springs, lengths = line.split(' ')
    lengths = [int(s) for s in lengths.split(',')]
    arrangements = count_arrangements(springs, tuple(lengths))
    logging.info("{} {} -> {} arrangements".format(springs, lengths, arrangements))
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

    # logging.debug("Checking {} -> {} {}".format(line, springs, lengths))
    arrangements = count_arrangements(springs, tuple(lengths))
    logging.info("{} -> {} {} -> {} arrangements".format(line, springs, lengths, arrangements))
    # logging.info("works: {}".format(works.cache_info()))
    # logging.info("count_arrangements: {}".format(count_arrangements.cache_info()))
    total_arrangements += arrangements

logging.info("Total arrangements: {}".format(total_arrangements))

if not TEST:
    p.answer_b = total_arrangements
