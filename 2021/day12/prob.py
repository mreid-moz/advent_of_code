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

def acceptable_path(path):
  logging.debug("Checking path {}".format("-".join(path)))
  for single in ['start', 'end']:
    if len([n for n in path if n == single]) > 1:
      return False
  smalls = [p for p in path if small(p) and p != 'start' and p != 'end']
  num_smalls = len(smalls)
  num_unique_smalls = len(set(smalls))
  if num_smalls <= num_unique_smalls + 1:
    logging.debug("Path was acceptable")
    return True
  logging.debug("Path was NOT acceptable")
  return False

def find_paths2(position, target, current_path):
  if position == target:
    return [current_path]

  paths = []
  for neighbour in cave_map[position]:
    if not acceptable_path(current_path + [position]):
      continue
    paths += find_paths2(neighbour, target, current_path + [position])
  return paths

p = find_paths2('start', 'end', [])
logging.info("Found {} paths through the cave".format(len(p)))
