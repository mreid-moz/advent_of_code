import logging
import re
import sys
logging.basicConfig(level=logging.INFO)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [l.strip() for l in fin.readlines()]

total_yeses = 0
current = set()

for line in my_input:
  if line == '':
    total_yeses += len(current)
    current = set()
  else:
    for a in line:
      current.add(a)

total_yeses += len(current)

logging.info("Found {} yeses".format(total_yeses))