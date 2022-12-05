from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2022, day=5)

lines = p.input_data.splitlines()

pattern = re.compile(r"move (\d+) from (\d) to (\d)")

stacks = []
for i in range(9):
  stacks.append([])

instructions = []

for line in lines:
  m = pattern.match(line)
  if m:
    count = int(m.group(1))
    from_stack = int(m.group(2)) - 1
    to_stack = int(m.group(3)) - 1
    instructions.append((count, from_stack, to_stack))
    continue
  for i, idx in enumerate([1,5,9,13,17,21,25,29,33]):
    if len(line) > idx and line[idx] != ' ':
      stacks[i].insert(0, line[idx])

# For part A, set to True
one_at_a_time = False
for count, from_stack, to_stack in instructions:
  if one_at_a_time:
    for i in range(count):
      crate = stacks[from_stack].pop()
      stacks[to_stack].append(crate)
  else:
    crates = stacks[from_stack][-1*count:]
    stacks[from_stack] = stacks[from_stack][0:len(stacks[from_stack]) - count]
    stacks[to_stack] = stacks[to_stack] + crates

tops = []
for stack in stacks:
  if len(stack) > 0:
    tops.append(stack[-1])

if one_at_a_time:
  p.answer_a = "".join(tops)
else:
  p.answer_b = "".join(tops)
