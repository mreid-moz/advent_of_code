from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2024, day=1)

TEST = False
if TEST:
    lines = p.examples[0].input_data.splitlines()
else:
    lines = p.input_data.splitlines()

a = []
b = []

for line in lines:
    l, r = line.split()
    a.append(int(l))
    b.append(int(r))

a.sort()
b.sort()

diffs = 0
for i in range(len(a)):
    diffs += abs(a[i] - b[i])

counts = defaultdict(int)
for bi in b:
    counts[bi] += 1

diffs2 = 0
for i in range(len(a)):
    diffs2 += a[i] * counts[a[i]]

if not TEST:
    p.answer_a = diffs
    p.answer_b = diffs2
