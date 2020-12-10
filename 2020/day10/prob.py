import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [int(l.strip()) for l in fin.readlines()]

chain = [0] + sorted(my_input)
chain.append(chain[-1] + 3)

one_diffs = 0
three_diffs = 0

for i in range(len(chain) - 1):
  diff = chain[i+1] - chain[i]
  if diff == 1:
    one_diffs += 1
  elif diff == 3:
    three_diffs += 1
  else:
    logging.debug("unexpected diff between chain[{}]={} and chain[{}]={} of {}.".format(i, chain[i], i+1, chain[i+1], diff))

logging.info("Part 1: Found {} diffs of 1, {} diffs of three, for an answer of {}".format(one_diffs, three_diffs, one_diffs * three_diffs))
