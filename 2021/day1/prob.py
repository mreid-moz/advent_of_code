import logging
import re
import sys

logging.basicConfig(level=logging.INFO)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [int(l.strip()) for l in fin.readlines()]

def count_increases_general(nums, window_size=1):
  base = nums[0:window_size]
  increases = 0
  for n in nums[window_size:]:
    prev = sum(base)
    curr = prev + n - base[0]
    if curr > prev:
      increases += 1
    base = base[1:] + [n]
  return increases

logging.info("Window of 1: {}. Window of 3: {}".format(
  count_increases_general(my_input),
  count_increases_general(my_input, 3)))
