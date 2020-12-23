import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [l.strip() for l in fin.readlines()]

def insert(s, sublist, offset):
  if offset < 0:
    offset += len(s)
  return s[:offset+1] + sublist + s[offset+1:]

def remove(s, index, length):
  if index + length > len(s):
    removed = s[index:] + s[:index + length - len(s)]
    remainder = s[index + length - len(s):index]
    return removed, remainder
  return s[index:index+length], s[:index] + s[index+length:]

def step_between(v, min_value, max_value, increment):
  n = v + increment
  if n < min_value:
    return max_value
  if n > max_value:
    return min_value
  return n

cups = [int(s) for s in my_input[0]]
n_cups = len(cups)

min_cup = cups[0]
max_cup = cups[0]
for cup in cups[1:]:
  if cup > max_cup:
    max_cup = cup
  if cup < min_cup:
    min_cup = cup

def print_cups(cups, current_cup):
  cup_strings = [str(s) for s in cups]
  cup_strings[current_cup] = '(' + cup_strings[current_cup] + ')'
  logging.debug("cups: {}".format(' '.join(cup_strings)))

current_cup = 0
move_num = 0
for i in range(100):
  move_num += 1
  logging.debug("-- move {} --".format(move_num))
  print_cups(cups, current_cup)
  destination_cup = cups[current_cup] - 1
  removed, cups = remove(cups, current_cup + 1, 3)
  logging.debug("pick up: {}".format(removed))
  while True:
    try:
      destination_idx = cups.index(destination_cup)
      break
    except ValueError:
      destination_cup = step_between(destination_cup, min_cup, max_cup, -1)
  logging.debug("destination: {} (index {})".format(destination_cup, destination_idx))
  cups = insert(cups, removed, destination_idx)

  # we moved some from after current cup to before
  if destination_idx < current_cup:
    # we can't move the current cup, so re-shuffle up to 3 items
    for _ in range(min(3, len(cups) - current_cup - 1)):
      cups.append(cups.pop(0))
  current_cup = step_between(current_cup, 0, n_cups - 1, 1)
logging.debug("Final")
print_cups(cups, current_cup)

def get_cups_after(cups, n):
  idx = cups.index(n)
  return cups[idx+1:] + cups[:idx]

logging.info("After {} moves, cups look like {}".format(move_num, ''.join(str(c) for c in get_cups_after(cups, 1))))

