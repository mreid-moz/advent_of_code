import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

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

window = list()
for i in range(preamble_length):
  window.append(int(my_input.pop(0)))

for s in my_input:
  n = int(s)
  if check(n, window):
    logging.debug("{} is valid using window [{}]".format(s, ", ".join([str(w) for w in window])))
  else:
    logging.info("Part 1: {} is not valid using window [{}]".format(s, ", ".join([str(w) for w in window])))
    invalid_input = int(s)
    break
  window.pop(0)
  window.append(n)

for i in range()