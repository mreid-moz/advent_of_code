import logging
import re
import sys

logging.basicConfig(level=logging.INFO)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [l.strip() for l in fin.readlines()]

gamma = ''
epsilon = ''
for i in range(len(my_input[0])):
  zero_count = 0
  one_count = 0
  for v in my_input:
    if v[i] == '0':
      zero_count += 1
    else:
      one_count += 1
  if zero_count > one_count:
    gamma += '0'
    epsilon += '1'
  else:
    gamma += '1'
    epsilon += '0'

b_gamma = int(gamma, 2)
b_epsilon = int(epsilon, 2)
logging.info("Part 1: power gamma={}, epsilon={}, consumption {}".format(gamma, epsilon, b_gamma * b_epsilon))

def is_one_common(values, position):
  zero_count = 0
  one_count = 0
  for v in values:
    if v[position] == '0':
      zero_count += 1
    else:
      one_count += 1

  return one_count - zero_count

def find_rating(values, position, common=True):
  logging.debug("Looking at values in position {}: {}".format(position, values))
  if len(values) == 1:
    return values[0]
  one_common = is_one_common(values, position)

  if common:
    if one_common >= 0:
      target = '1'
    else:
      target = '0'
  else:
    if one_common < 0:
      target = '1'
    else:
      target = '0'

  return find_rating([v for v in values if v[position] == target], position + 1, common)

o2_rating = find_rating(my_input, 0, True)
co2_rating = find_rating(my_input, 0, False)
b_o2 = int(o2_rating, 2)
b_co2 = int(co2_rating, 2)
logging.info("Part 2: power o2_rating={}, co2_rating={}, consumption {}".format(o2_rating, co2_rating, b_o2 * b_co2))

