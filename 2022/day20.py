from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

puzz = Puzzle(year=2022, day=20)

TEST = False
# TEST = True

if TEST:
  # lines = ["1", "2", "-3", "3", "-2", "0", "4"]
  lines = ["1", "2", "-5", "-10", "10", "9", "0", "8", "-9", "3"]
else:
  lines = puzz.input_data.splitlines()

lines = [int(s) for s in lines]

v_to_p = {}
p_to_v = {}

for p, v in enumerate(lines):
  v_to_p[v] = p
  p_to_v[p] = v

def get_coords(v_to_p, p_to_v):
  lv = len(v_to_p)
  zero_idx = v_to_p[0]

  logging.info(f"Found zero at {zero_idx}")

  a = p_to_v[(1000 + zero_idx) % lv]
  b = p_to_v[(2000 + zero_idx) % lv]
  c = p_to_v[(3000 + zero_idx) % lv]
  logging.info(f"1000: {a}, 2000: {b}, 3000: {c}; coord={a+b+c}")
  return a + b + c

def mix(values):
  lv = len(values)
  values_orig = values[:]
  for v in values:
    old_pos = v_to_p[v]
    if v > 0:
      new_pos = v_to_p[v] + v
    elif v < 0:
      new_pos = v_to_p[v] + v - 1
    else:
      new_pos = old_pos

    if new_pos < 0:
      new_pos %= lv
    #   # new_pos -= 1

    if new_pos >= lv:
      new_pos %= lv
      new_pos += 1

    logging.debug(f"Moving {v} from {old_pos} to {new_pos}")

    if new_pos < old_pos: # moved to the left
      for i in range(old_pos - 1, new_pos - 1, -1):
        mv = p_to_v[i]
        # logging.debug(f"then, moving {mv} right from {i + 1} to {i}")
        p_to_v[i+1] = mv
        v_to_p[mv] = i+1
        # v_to_p[v] = new_pos
        # p_to_v[new_pos] = v
    elif new_pos > old_pos: # moved to the right
      for i in range(old_pos+1, new_pos+1):
        mv = p_to_v[i]
        # logging.debug(f"then, moving {mv} left from {i} to {i-1}")
        p_to_v[i-1] = mv
        v_to_p[mv] = i-1
        # v_to_p[v] = new_pos
        # p_to_v[new_pos] = v
        # logging.debug(f"R New list: {[p_to_v[i] for i in range(lv)]}")
    else:
      # logging.debug("v was zero, no change")
      pass
    v_to_p[v] = new_pos
    p_to_v[new_pos] = v
    logging.debug(f"New list: {[p_to_v[i] for i in range(lv)]}")

logging.info(f"Found {len(lines)} lines.")
mix(lines)
coords = get_coords(v_to_p, p_to_v)
logging.info(coords)
if not TEST:
  puzz.answer_a = coords
