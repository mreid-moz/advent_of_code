from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.INFO)

p = Puzzle(year=2024, day=9)

TEST = False
if TEST:
    lines = p.examples[0].input_data.splitlines()
else:
    lines = p.input_data.splitlines()

def convert(line):
    digits = [int(s) for s in line]
    d = digits.pop(0)
    converted = [0] * d
    num = 0
    while(digits):
        num += 1
        spaces = digits.pop(0)
        converted += [None] * spaces
        d = digits.pop(0)
        converted += [num] * d
    return converted

def defrag(frag):
    target = 0
    source = len(frag) - 1
    while source >= target:
        while frag[target] is not None:
            target += 1
        while frag[source] is None:
            source -= 1
        if source >= target:
            frag[target] = frag[source]
            frag[source] = None

def checksum(defrag):
    sum = 0
    for i in range(len(defrag)):
        if defrag[i] is None:
            continue
        sum += i * defrag[i]
    return sum

fragmented = convert(lines[0])
logging.debug(f"{lines[0]} -> {fragmented}")
defrag(fragmented)
logging.debug(fragmented)
cs = checksum(fragmented)
logging.info(f"Checksum is {cs}")

if not TEST:
    p.answer_a = cs

# Use a different representation for part 2:
# a list of (type, file id, number of blocks)
# where type is 'f' for files or 's' for spaces
def convert2(line):
    digits = [int(s) for s in line]
    d = digits.pop(0)
    converted = [('f', 0, d)]
    num = 0
    while(digits):
        num += 1
        spaces = digits.pop(0)
        converted.append(('s', None, spaces))
        d = digits.pop(0)
        converted.append(('f', num, d))
    return converted

def defrag2(frag):
    files = reversed([f for f in frag if f[0] == 'f'])
    for t, d, n in files:
        logging.debug(f"Moving file {d} ({n})")
        for i in range(len(frag)):
            if frag[i][0] == 's' and frag[i][2] >= n:
                # put it here.
                prev_idx = frag.index((t, d, n))
                if prev_idx < i:
                    break
                frag[prev_idx] = ('s', None, n)
                new_space = frag[i][2] - n
                logging.debug(f"moving {d} from {prev_idx} to {i}")
                if new_space > 0:
                    frag[i] = ('s', None, new_space)
                    # Don't worry about combining later spaces into one big space.
                    # We only move things once, and only to the left.
                    frag.insert(i, (t, d, n))
                else:
                    frag[i] = (t, d, n)
                break

# Turn it back into the part1 representation for
# computing the checksum
def flatten(p2):
    flat = []
    for t, d, n in p2:
        flat += [d] * n
    return flat

fragmented = convert2(lines[0])
logging.debug(f"{lines[0]} -> {fragmented}")
defrag2(fragmented)
logging.debug(fragmented)
flat = flatten(fragmented)
logging.debug(flat)
cs = checksum(flat)
logging.info(f"Part 2: Checksum is {cs}")

if not TEST:
    p.answer_b = cs
