import logging
import copy
import re
import sys
from collections import deque
from functools import reduce

logging.basicConfig(level=logging.INFO)

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

  def root(self):
    current = self
    while current.parent is not None:
      current = current.parent
    return current

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

def get_neighbour(root, target, side='right'):
  logging.debug(f"{root} -> Finding {side} neighbour of {target}")
  if root is None:
    return None
  q = deque()
  q.append(root)
  while len(q) > 0:
    logging.debug("Deque contained {}".format(" / ".join([str(n) for n in q])))
    sz = len(q)
    for i in range(sz):
      p = q.popleft()
      logging.debug(f"Checking if {p} == {target}")
      if p == target:
        logging.debug("it was")
        if i == sz - 1:
          logging.debug("but there wasn't anything good in the queue")
          return None
        neighbour = q.popleft()
        logging.debug(f"Found {side} neighbour of {target}: {neighbour}")
        return neighbour
      if side == 'right':
        if p.left:
          logging.debug(f"enqueing left: {p.left}")
          q.append(p.left)
        if p.right:
          logging.debug(f"enqueing right: {p.right}")
          q.append(p.right)
      else:
        if p.right:
          logging.debug(f"enqueing right: {p.right}")
          q.append(p.right)
        if p.left:
          logging.debug(f"enqueing left: {p.left}")
          q.append(p.left)
  return None

def flatten(root):
  flat = []
  if root.left:
    flat += flatten(root.left)
  flat.append(root)
  if root.right:
    flat += flatten(root.right)
  return flat

def explode(pair, depth=0):
  logging.debug(f"exploding {pair} at depth {depth}")
  if depth == 4 and pair.v is None:
    logging.debug("this one should explode.")

    # These will always be actual values
    left_value = pair.left.v
    right_value = pair.right.v
    parent = pair.parent
    root = pair.root()
    flat = flatten(root)
    first_left = None
    first_right = None
    pair_idx = -1
    for i, n in enumerate(flat):
      logging.debug(f"Flattened[{i}] = {n}")
      if n.v is not None and n != pair.left:
        first_left = n
      if n == pair:
        pair_idx = i
        break

    for i in range(pair_idx + 2, len(flat)):
      n = flat[i]
      logging.debug(f"Flattened[{i}] = {n}")
      if n.v is not None and n != pair.right:
        first_right = n
        break

    logging.debug(f"Pair: {pair}, first left: {first_left}, first_right: {first_right}")

    if first_left is None:
      logging.debug("no value to the left")
    else:
      first_left.v += left_value

    if first_right is None:
      logging.debug("no value to the right")
    else:
      first_right.v += pair.right.v

    if parent.left == pair:
      parent.left = Pair(0, parent=parent)
    else:
      parent.right = Pair(0, parent=parent)

    return True
  if pair.left is not None:
    if explode(pair.left, depth+1):
      return True
  if pair.right is not None:
    if explode(pair.right, depth+1):
      return True
  return False






