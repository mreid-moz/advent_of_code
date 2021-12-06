import logging
import copy
import sys
from collections import defaultdict

logging.basicConfig(level=logging.INFO)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [l.strip() for l in fin.readlines()]

initial_state = [int(v) for  v in my_input[0].split(',')]

def to_s(state):
  return ",".join([str(s) for s in state])

def step(state):
  num_new = 0
  for i, fish in enumerate(state):
    if fish == 0:
      state[i] = 6
      num_new += 1
    else:
      state[i] -= 1
  state += [8] * num_new
  return state


logging.info("Initial state: {}".format(to_s(initial_state)))

current_state = copy.deepcopy(initial_state)
for i in range(80):
  current_state = step(current_state)
  logging.debug("After {} days: {}".format(i + 1, to_s(current_state)))

logging.info("After {} days, there are {} fish".format(i+1, len(current_state)))


current_state = copy.deepcopy(initial_state)
for i in range(256):
  logging.info("processed {} days, so far there are {} fish".format(i, len(current_state)))
  current_state = step(current_state)
  logging.debug("After {} days: {}".format(i + 1, to_s(current_state)))

logging.info("After {} days, there are {} fish".format(i+1, len(current_state)))