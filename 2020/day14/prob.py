import logging
import re
import sys

from collections import defaultdict

logging.basicConfig(level=logging.DEBUG)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [l.strip() for l in fin.readlines()]

def apply_mask(m, val):
  logging.debug("Applying mask:   {} to {}".format(m, val))
  val_as_binary = "{0:036b}".format(int(val))
  logging.debug("As binary:       {}".format(val_as_binary))
  masked = list(val_as_binary)
  for i, bit in enumerate(m):
    if bit != 'X':
      masked[i] = bit

  bits = ''.join(masked)
  as_int = int(bits, 2)
  logging.debug("Resulting value: {} ({})".format(bits, as_int))
  return as_int

mask = None
mask_pattern = re.compile('^mask = (?P<mask>[X01]+)$')
mem_pattern = re.compile('^mem\[(?P<mem>[0-9]+)\] = (?P<val>[0-9]+)$')

mem = defaultdict(int)
for line in my_input:
  match = mask_pattern.match(line)
  if match:
    mask = match.group('mask')
  else:
    match = mem_pattern.match(line)
    if match:
      mem[match.group('mem')] = apply_mask(mask, match.group('val'))
    else:
      logging.info("Unmatched line: {}".format(line))

logging.info("Part 1: sum of values was {}".format(sum(mem.values())))
