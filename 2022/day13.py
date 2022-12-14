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

def compare(left, right):
  logging.debug(f"Comparing {left} vs {right}")
  if not left and not right:
    logging.debug("Maybe: both empty")
    return 0
  if not left and right:
    logging.debug("Ordered: left empty, right not empty")
    return 1
  if not right:
    logging.debug("Not: left not empty, right empty")
    return -1

  left_item = left.pop(0)
  right_item = right.pop(0)

  logging.debug(f"comparing first item {left_item} to {right_item}")
  if isinstance(left_item, int):
    # left int
    if isinstance(right_item, int):
      # left int, right int
      if left_item < right_item:
        logging.debug("Ordered: left < right")
        return 1
      elif left_item == right_item:
        logging.debug("Same: left == right, keep looking!")
        return compare(left, right)
      if right_item < left_item:
        logging.debug("Not: right int was smaller")
        return -1
    else:
      # left int, right list
      logging.debug("Making left item into a list")
      result = compare([left_item], right_item)
      if result < 0:
        logging.debug("Not: list compare not ordered")
        return result
      elif result > 0:
        logging.debug("Ordered: list compare was ordered")
        return result
      else:
        return compare(left, right)
  else:
    # left list
    if isinstance(right_item, int):
      # left list, right int
      logging.debug("Making right item into a list")
      result = compare(left_item, [right_item])
      if result < 0:
        return result
      elif result > 0:
        return result
      else:
        return compare(left, right)
    else:
      # left list, right list
      result = compare(left_item, right_item)
      if result < 0:
        return result
      elif result > 0:
        return result
      else:
        return compare(left, right)

  if not left and not right:
    # nothing left to check
    logging.debug("Maybe: Nothing left to check")
    return 0
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
  if compare(left, right) == 1:
    result = "Ordered"
    ordered_indices.append(i+1)
  logging.debug(f"Pair {i+1}: {result}")

logging.info(f"Sum of ordered indices: {sum(ordered_indices)}")

if not TEST:
  p.answer_a = sum(ordered_indices)
