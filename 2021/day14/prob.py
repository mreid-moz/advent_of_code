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
  rules[pair] = insertion

def apply(start, rules):
  after = start[0]
  for i in range(1, len(start)):
    pair = after[-1] + start[i]
    after += rules[pair]
    after += start[i]
  return after

last = template
for i in range(10):
  last = apply(last, rules)

counts = defaultdict(int)
for c in last:
  counts[c] += 1

min_count = min(counts.values())
max_count = max(counts.values())

logging.info("After {} iterations, we get {} - {} = {}".format(
  i+1, max_count, min_count, max_count - min_count))