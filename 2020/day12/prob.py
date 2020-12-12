import logging
from nav import Nav
import sys

logging.basicConfig(level=logging.INFO)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [l.strip() for l in fin.readlines()]

n = Nav()
for line in my_input:
  n.move(line)

logging.info("Part 1: manhattan distance {}".format(n.manhattan()))