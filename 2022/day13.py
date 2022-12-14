from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2022, day=13)

TEST = False
# TEST = True

if TEST:
  lines = [
    "[1,1,3,1,1]",
    "[1,1,5,1,1]",
    "",
    "[[1],[2,3,4]]",
    "[[1],4]",
    "",
    "[9]",
    "[[8,7,6]]",
    "",
    "[[4,4],4,4]",
    "[[4,4],4,4,4]",
    "",
    "[7,7,7,7]",
    "[7,7,7]",
    "",
    "[]",
    "[3]",
    "",
    "[[[]]]",
    "[[]]",
    "",
    "[1,[2,[3,[4,[5,6,7]]]],8,9]",
    "[1,[2,[3,[4,[5,6,0]]]],8,9]",
    "",
    "[[0]]",
    "[[1]]",
    "",
    "[[1]]",
    "[[0]]",
    "",
    "[[0, 0]]",
    "[[0, 1]]",
    "",
    "[[0, 1]]",
    "[[1, 0]]",
    "",
    "[[0, 1]]",
    "[[0, 0]]",
  ]
else:
  lines = p.input_data.splitlines()


def all_ints(mixed):
  if not mixed:
    return False
  for item in mixed:
    if not isinstance(item, int):
      return False
  return True

def compare(left, right):
  logging.debug(f"Comparing {left} vs {right}")
  if not left and right:
    logging.debug("Ordered: left empty, right not empty")
    return True

  if not right:
    logging.debug("Not: left not empty, right empty")
    return False
  left_item = left.pop(0)
  right_item = right.pop(0)
  if isinstance(left_item, int):
    # left int
    if isinstance(right_item, int):
      # left int, right int
      if left_item < right_item:
        logging.debug("Ordered: left int was smaller")
        return True
      if right_item < left_item:
        logging.debug("Not: right int was smaller")
        return False
      if not right and all_ints(left):
        logging.debug("Ran out of items on the right, all ints on the left")
        if left_item < right_item:
          return True
        elif right_item < left_item:
          return False
        else:
          logging.debug("SAME")
    else:
      # left int, right list
      return compare([left_item], right_item)
  else:
    # left list
    if isinstance(right_item, int):
      # left list, right int
      return compare(left_item, [right_item])
    else:
      # left list, right list
      if all_ints(left_item) and all_ints(right_item):
        logging.debug("Comparing 2 int lists")
        lr = len(right_item)
        for i, l in enumerate(left_item):
          if i >= lr:
            logging.debug("Not: ran out of items on the right")
            return False
          if l <= right_item[i]:
            logging.debug("found a lower int on the left")
            # this is ok, keep checking more items.
          elif l > right_item[i]:
            logging.debug("not ordered: found a lower int on the right")
            return False
          else:
            logging.warning("impossible!")
        return True
      # if not compare(left_item, right_item):
      #   return False
      return compare(left_item, right_item)


  if not left and not right:
    # nothing left to check
    logging.debug("Ordered Nothing left to check")
    return True
  else:
    return compare(left, right)

pairs = []
current_pair = []
for line in lines:
  if line == '':
    pairs.append(current_pair)
    current_pair = []
  else:
    current_pair.append(eval(line))
pairs.append(current_pair)

ordered_indices = []
for i in range(0, len(pairs)):
  left, right = pairs[i]
  result = "Not"
  if compare(left, right):
    result = "Ordered"
    ordered_indices.append(i+1)
  logging.debug(f"Pair {i+1}: {result}")

logging.info(f"Sum of ordered indices: {sum(ordered_indices)}")

if not TEST:
  p.answer_a = sum(ordered_indices)
