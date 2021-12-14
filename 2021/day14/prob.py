import logging
import copy
import re
import sys
from collections import defaultdict

logging.basicConfig(level=logging.INFO)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [l.strip() for l in fin.readlines()]

template = my_input[0]
rule_lines = my_input[2:]
rules = {}
for r in rule_lines:
  pair, insertion = r.split(' -> ')
  rules[pair] = (pair[0] + insertion, insertion + pair[1])

def apply(start, rules):
  after = defaultdict(int)
  for pair, count in start.items():
    v1, v2 = rules[pair]
    after[v1] += count
    after[v2] += count
  return after

def get_counts(state):
  counts = defaultdict(int)
  # always starts with the same character
  counts[template[0]] += 1
  for k, v in state.items():
    counts[k[1]] += v
  return (min(counts.values()), max(counts.values()))

current_state = defaultdict(int)
for i in range(len(template) - 1):
  current_state[template[i] + template[i+1]] += 1
logging.debug("Initial state:")
for k, v in current_state.items():
    logging.debug("{} -> {}".format(k, v))

for i in range(40):
  current_state = apply(current_state, rules)

  logging.debug("After {} steps: length {}".format(i+1, sum(current_state.values()) + 1))
  if i == 9:
    min_count, max_count = get_counts(current_state)
    logging.info("After {} iterations, we get {} - {} = {}".format(
  i+1, max_count, min_count, max_count - min_count))
  for k, v in current_state.items():
    logging.debug("{} -> {}".format(k, v))

min_count, max_count = get_counts(current_state)
logging.info("After {} iterations, we get {} - {} = {}".format(
  i+1, max_count, min_count, max_count - min_count))