import logging
import re
import sys

from collections import defaultdict

logging.basicConfig(level=logging.INFO)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [l.strip() for l in fin.readlines()]

def apply_mask(mask, val):
  logging.debug("Applying mask:   {} to {}".format(mask, val))
  val_as_binary = "{0:036b}".format(int(val))
  logging.debug("As binary:       {}".format(val_as_binary))
  masked = list(val_as_binary)
  for i, bit in enumerate(mask):
    if bit != 'X':
      masked[i] = bit

  bits = ''.join(masked)
  as_int = int(bits, 2)
  logging.debug("Resulting value: {} ({})".format(bits, as_int))
  return as_int

def generate_addresses(masked, floaters):
  logging.debug("Generating addresses for {} with keys {}".format(''.join(masked), floaters))
  addresses = list()
  count = len(floaters)
  for i in range(2 ** count):
    s = ("{0:0" + str(count) + "b}").format(i)
    logging.debug("Applying values {}".format(s))
    tmp = masked.copy()
    for src, target in list(zip(range(count), floaters)):
      tmp[target] = s[src]
      logging.debug("Setting position {} to {}[{}] = {}".format(target, s, src, s[src]))
    bits = ''.join(tmp)
    addresses.append(int(bits, 2))
  return addresses

def get_addresses(mask, address):
  address_as_binary = "{0:036b}".format(int(address))
  masked = list(address_as_binary)
  floaters = set()
  for i, bit in enumerate(mask):
    if bit == '1':
      masked[i] = bit
    elif bit == 'X':
      masked[i] = bit
      floaters.add(i)
  return generate_addresses(masked, floaters)

mask = None
mask_pattern = re.compile('^mask = (?P<mask>[X01]+)$')
mem_pattern = re.compile('^mem\[(?P<mem>[0-9]+)\] = (?P<val>[0-9]+)$')

mem = defaultdict(int)
mem2 = defaultdict(int)
for line in my_input:
  match = mask_pattern.match(line)
  if match:
    mask = match.group('mask')
  else:
    match = mem_pattern.match(line)
    if match:
      mem[match.group('mem')] = apply_mask(mask, match.group('val'))
      for a in get_addresses(mask, match.group('mem')):
        mem2[a] = int(match.group('val'))
    else:
      logging.info("Unmatched line: {}".format(line))

logging.info("Part 1: sum of values was {}".format(sum(mem.values())))
logging.info("Part 2: sum of values was {}".format(sum(mem2.values())))
