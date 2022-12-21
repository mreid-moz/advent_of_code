from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.INFO)

puzz = Puzzle(year=2022, day=20)

TEST = False
# TEST = True

if TEST:
  lines = ["1", "2", "-3", "3", "-2", "0", "4"]
else:
  lines = puzz.input_data.splitlines()

lines = [int(s) for s in lines]

class Node:
  def __init__(self, value):
    self.v = value
    self.next = None
    self.previous = None

  def insert_after(self, other_node):
    #   self -> self.next
    #   self -> other -> self.next
    if self.next:
      self.next.previous = other_node
    other_node.previous = self
    other_node.next = self.next
    self.next = other_node

  def insert_before(self, other_node):
    #   self.previous -> self
    #   self.previous -> other -> self
    if self.previous:
      self.previous.next = other_node
    other_node.next = self
    other_node.previous = self.previous
    self.previous = other_node

  def remove(self):
    # previous -> self -> next
    # previous -> next
    prev = self.previous
    if self.previous:
      self.previous.next = self.next
    else:
      logging.warning(f"previous node was None: {self}")

    if self.next:
      self.next.previous = self.previous
    else:
      logging.warning(f"next node was None: {self}")
    self.previous = None
    self.next = None
    return prev

  def __str__(self):
    prev_str = 'None'
    next_str = 'None'
    if self.previous:
      prev_str = str(self.previous.v)
    if self.next:
      next_str = str(self.next.v)
    return f"...{prev_str} -> {self.v} -> {next_str}..."

def stringify(a_list):
  start = a_list
  nodes = [a_list.v]
  while True:
    a_list = a_list.next
    if a_list is None or a_list == start:
      break
    nodes.append(a_list.v)
  return ','.join([str(s) for s in nodes])

def make_list(values):
  start = Node(lines[0])
  zero = None

  node_map = {}
  node_map[(0, start.v)] = start

  last_node = start
  for i, v in enumerate(lines[1:]):
    n = Node(v)
    if v == 0:
      if zero is not None:
        logging.warning(f"Found another zero on line {i+1}")
      zero = n
    node_map[(i+1, v)] = n
    last_node.insert_after(n)
    last_node = last_node.next
  last_node.next = start
  start.previous = last_node

  return node_map, start, zero

node_map, start, zero = make_list(lines)

logging.debug(f"Initial list: {stringify(start)}")

def find(start, value):
  current = start
  while current.v != value:
    current = current.next
  return current

def get_coords(start, key=1):
  zero_node = find(start, 0)
  next_node = zero_node
  for i in range(1000):
    next_node = next_node.next
  v1k = next_node.v * key
  for i in range(1000):
    next_node = next_node.next
  v2k = next_node.v * key
  for i in range(1000):
    next_node = next_node.next
  v3k = next_node.v * key

  logging.info(f"1000: {v1k}, 2000: {v2k}, 3000: {v3k}; coord={v1k+v2k+v3k}")
  return v1k+v2k+v3k

def mix(values, key=1):
  for vi, v in enumerate(values):
    if v == 0:
      logging.debug("skipping moving zero")
      continue
    v_node = node_map[(vi, v)]
    logging.debug(f"Found node for ({vi},{v}): {v_node}")
    current_node = v_node.remove()
    logging.debug(f"Current node: {current_node}")
    v *= key
    if v > 0:
      num_moves = v % (len(values) - 1)
      for i in range(num_moves):
        current_node = current_node.next
      current_node.insert_after(v_node)
    elif v < 0:
      num_moves = abs(v) % (len(values) - 1)
      for i in range(num_moves):
        current_node = current_node.previous
      current_node.insert_after(v_node)

    logging.debug(f"Moved {vi}:{v} between {v_node.previous.v} and {v_node.next.v}")
    logging.debug(f"New list: {stringify(start)}")

logging.info(f"Found {len(lines)} lines.")
mix(lines)
logging.debug(f"After mixing: {stringify(start)}")

coords = get_coords(start)
logging.info(coords)
if not TEST:
  puzz.answer_a = coords

### part b
node_map, start, zero = make_list(lines)
logging.debug(f"Part 2, before mixing: {stringify(start)}")

for i in range(10):
  mix(lines, key=811589153)
  logging.info(f"Mixed {i+1} times.")
  logging.debug(f"After mixing {i+1} times: {stringify(start)}")

coords = get_coords(start, key=811589153)
logging.info(f"Part 2: coords = {coords}")
if not TEST:
  puzz.answer_b = coords
