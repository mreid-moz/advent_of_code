import logging
import copy
import re
import sys
from collections import defaultdict
from functools import reduce

logging.basicConfig(level=logging.DEBUG)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [l.strip() for l in fin.readlines()]

class Pair:
  def __init__(self, v=None, left=None, right=None, parent=None):
    self.v = v
    self.left = left
    self.right = right
    self.parent = parent

  def __str__(self):
    if self.left is None and self.right is None:
      return str(self.v)
    return f"[{self.left},{self.right}]"

def parse(line):
  middle = -1
  open_counter = 0
  for i, c in enumerate(line):
    if c == '[':
      open_counter += 1
    elif c == ']':
      open_counter -= 1
    elif c == ',' and open_counter == 1:
      # 1 accounts for the initial opening bracket.
      middle = i

  left = line[1:middle]
  right = line[middle+1:-1]
  #logging.debug(f"{line} -> L: {left}, R: {right}")

  if re.match(r'[0-9]+', left):
    left = Pair(int(left))
  else:
    left = parse(left)

  if re.match(r'[0-9]+', right):
    right = Pair(int(right))
  else:
    right = parse(right)

  p = Pair(left=left, right=right)
  left.parent = p
  right.parent = p
  return p

def get_first_left(pair, depth):
  parent = pair.parent
  for i in range(depth):
    if parent is None:
      return None
    if parent.left.v is not None:
      return parent.left
    parent = parent.parent
  return None

def get_first_right(pair, depth):
  logging.debug(f"Seeking a right for {pair}")
  parent = pair.parent
  for i in range(depth + 5):
    if parent is None:
      logging.debug(f"Hit the root, stopping")
      return None
    if parent.right.v is not None:
      logging.debug(f"Found a right value: {parent.right}")
      return parent.right
    parent = parent.parent
  return None

def explode(pair, depth=0):
  logging.debug(f"exploding {pair} at depth {depth}")
  if depth == 4 and pair.v is None:
    logging.debug("this one should explode.")

    # These will always be actual values
    left_value = pair.left.v
    right_value = pair.right.v

    parent = pair.parent



    first_left = get_first_left(pair, depth)
    logging.debug(f"Pair: {pair}, first left: {first_left}")
    if first_left is None:
      logging.debug("no value to the left")
      parent.left = Pair(0, parent=parent)
    else:
      if first_left == parent:
        parent.left = Pair(first_left.v + pair.left.v, parent=parent)
      else:
        first_left.v += pair.left.v

    first_right = get_first_right(pair, depth)
    logging.debug(f"Pair: {pair}, first right: {first_right}")
    if first_right is None:
      logging.debug("no value to the right")
      parent.right = Pair(0, parent=parent)
    else:
      if first_right == parent:
        logging.debug("first right is parent")
        parent.right = Pair(first_right.v + pair.right.v, parent=parent)
      else:
        logging.debug("first right is not parent")
        first_right.v += pair.right.v
        #parent.right = Pair(0, parent=parent)

    return True
  if pair.left is not None:
    if explode(pair.left, depth+1):
      return True
  if pair.right is not None:
    if explode(pair.right, depth+1):
      return True
  return False