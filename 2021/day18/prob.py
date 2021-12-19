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

  def magnitude(self):
    if self.v is not None:
      return self.v

    return (self.left.magnitude() * 3) + (self.right.magnitude() * 2)

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

def flatten(root):
  flat = []
  if root.left:
    flat += flatten(root.left)
  flat.append(root)
  if root.right:
    flat += flatten(root.right)
  return flat

def explode(pair, depth=0):
  if depth == 4 and pair.v is None:
    #logging.debug("this one should explode.")

    # These will always be actual values
    left_value = pair.left.v
    right_value = pair.right.v
    parent = pair.parent
    root = pair.root()
    flat = flatten(root)
    logging.debug("Flattened {} to {}".format(root, [str(n) for n in flat]))
    first_left = None
    first_right = None
    pair_idx = -1
    for i, n in enumerate(flat):
      #logging.debug(f"Flattened[{i}] = {n}")
      if n.v is not None and n != pair.left:
        first_left = n
      if n == pair:
        pair_idx = i
        break

    for i in range(pair_idx + 2, len(flat)):
      n = flat[i]
      #logging.debug(f"Flattened[{i}] = {n}")
      if n.v is not None:# and n != pair.right:
        first_right = n
        break

    #logging.debug(f"Pair: {pair}, first left: {first_left}, first_right: {first_right}")

    if first_left is None:
      logging.debug("no value to the left")
    else:
      first_left.v += left_value

    if first_right is None:
      logging.debug("Flat {}: {}".format(pair_idx, [str(n) for n in flat]))
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


def split(pair):
  #logging.debug(f"splitting {pair}")
  if pair.v is not None and pair.v >= 10:
    #logging.debug("this one should split.")

    new_left = pair.v // 2
    new_right = new_left + (pair.v % 2)

    logging.debug(f"Splitting {pair.v} into ({new_left},{new_right})")

    pair.left = Pair(new_left, parent=pair)
    pair.right = Pair(new_right, parent=pair)
    pair.v = None
    return True
  if pair.left is not None:
    if split(pair.left):
      return True
  if pair.right is not None:
    if split(pair.right):
      return True
  return False

def add(p1, p2):
  p = Pair(left=p1, right=p2)
  p1.parent = p
  p2.parent = p
  return p

def reduce_snailfish(root):
  while True:
    logging.debug(f"Reducing {root}")
    exploded = explode(root, 0)
    if exploded:
      logging.debug("exploded.")
      continue
    splitted = split(root)
    if splitted:
      logging.debug("splitted.")
    if not splitted and not exploded:
      break
  logging.debug(f"After reducing: {root}")


if __name__ == "__main__":
  root = parse(my_input[0])
  logging.debug(f"Starting snailfish: {root}")
  for line in my_input[1:]:
    next_snailfish = parse(line)
    logging.debug(f"next snailfish: {next_snailfish}")
    root = add(root, next_snailfish)
    logging.debug(f"New snailfish: {root}")
    reduce_snailfish(root)
  logging.info(f"Part 1: Final list: {root}, magnitude is {root.magnitude()}")

  big = 0
  sailfishies = [parse(line) for line in my_input]
  for i, line1 in enumerate(my_input):
    for j, line2 in enumerate(my_input[i+1:]):
      logging.info(f"Checking {i} + {j}")
      added = add(parse(line1), parse(line2))
      reduce_snailfish(added)
      magnitude = added.magnitude()
      if magnitude > big:
        logging.info(f"Found a new max magnitude {magnitude} with {i} + {j}")
        big = magnitude

      logging.info(f"Checking {j} + {i}")
      added = add(parse(line2), parse(line1))
      reduce_snailfish(added)
      magnitude = added.magnitude()
      if magnitude > big:
        logging.info(f"Found a new max magnitude {magnitude} with {j} + {i}")
        big = magnitude

  logging.info(f"Part 2: Max magnitude: {big}")
