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

state = defaultdict(int)
for crab in initial_state:
  state[crab] += 1

def cost(state, target):
  c = 0
  for k, v in state.items():
    c += (abs(target - k) * v)
  return c

def cost2(state, target):
  c = 0
  for k, v in state.items():
    n = abs(target - k)
    # https://en.wikipedia.org/wiki/1_%2B_2_%2B_3_%2B_4_%2B_%E2%8B%AF
    c += ((n * (n+1))/2) * v
  return c

v_min = 999999
v_max = 0
for k, v in state.items():
  if k < v_min:
    v_min = k
  if k > v_max:
    v_max = k

min_cost = cost(state, 0)
for i in range(v_min, v_max + 1):
  current_cost = cost(state, i)
  if current_cost < min_cost:
    min_cost = current_cost

logging.info("Min cost: {}".format(min_cost))

min_cost = cost2(state, 0)
for i in range(v_min, v_max + 1):
  current_cost = cost2(state, i)
  if current_cost < min_cost:
    min_cost = current_cost

logging.info("Min cost2: {}".format(min_cost))
