import logging
import re
import sys

logging.basicConfig(level=logging.INFO)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [l.strip() for l in fin.readlines()]

preamble_length = 5
if input_file == 'input':
  preamble_length = 25

def check(n, window):
  for i in range(len(window)):
    for j in range(i+1, len(window)):
      if window[i] + window[j] == n:
        return True
  return False

window = [int(s) for s in my_input[0:preamble_length]]

for s in my_input[preamble_length:]:
  n = int(s)
  if check(n, window):
    logging.debug("{} is valid using window [{}]".format(s, ", ".join([str(w) for w in window])))
  else:
    logging.info("Part 1: {} is not valid using window [{}]".format(s, ", ".join([str(w) for w in window])))
    invalid_input = int(s)
    break
  window.pop(0)
  window.append(n)

for i in range(len(my_input)):
  total = int(my_input[i])
  j = i + 1
  logging.debug("looking for a contiguous blob starting at {} ({})".format(i, total))
  while total < invalid_input and j < len(my_input):
    total += int(my_input[j])
    logging.debug("item {} brings total to {}".format(j, total))
    j += 1
  if total == invalid_input:
    # add lowest and highest.
    items = sorted([int(s) for s in my_input[i:j]])
    logging.info("Part 2: found it, {} + {} = {}".format(items[0], items[-1], items[0] + items[-1]))
    break
