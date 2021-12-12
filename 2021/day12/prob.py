import logging
import copy
import sys
from collections import defaultdict
from functools import reduce

logging.basicConfig(level=logging.INFO)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [l.strip() for l in fin.readlines()]

def small(cave):
  return cave == cave.lower()

cave_map = defaultdict(set)

for line in my_input:
  a, b = line.split('-')
  cave_map[a].add(b)
  if a != 'start' and b != 'end':
    cave_map[b].add(a)

def find_paths(position, target, current_path):
  if position == target:
    return [current_path]

  paths = []
  for neighbour in cave_map[position]:
    if neighbour in current_path and small(neighbour):
      continue
    paths += find_paths(neighbour, target, current_path + [position])
  return paths

p = find_paths('start', 'end', [])
logging.info("Found {} paths through the cave".format(len(p)))

