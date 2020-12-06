import collections
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

def count_common_answers(d):
  group_size = d.get('group_size')
  common_answers = 0
  for k, v in d.items():
    if k == 'group_size':
      continue
    elif v == group_size:
      common_answers += 1
  return common_answers

common_yeses = 0
current = collections.defaultdict(int)

for line in my_input:
  if line == '':
    common_yeses += count_common_answers(current)
    current = collections.defaultdict(int)
  else:
    current['group_size'] += 1
    for a in line:
      current[a] += 1

common_yeses += count_common_answers(current)
logging.info("Found {} common yeses".format(common_yeses))