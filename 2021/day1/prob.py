import logging
import re
import sys

logging.basicConfig(level=logging.INFO)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [int(l.strip()) for l in fin.readlines()]

def count_increases(nums):
  base = -1
  increases = 0
  for n in nums:
    if base >= 0 and n > base:
      increases += 1
    base = n
  return increases

increases = count_increases(my_input)

logging.info("Part 1: depth increased {} times".format(increases))

def count_increases3(nums):
  b1 = nums[0]
  b2 = nums[1]
  b3 = nums[2]
  increases = 0
  for n in nums[3:]:
    prev = b1 + b2 + b3
    curr = prev + n - b1
    if curr > prev:
      increases += 1
    b1 = b2
    b2 = b3
    b3 = n
  return increases

logging.info("Part 2: depth increased {} times".format(count_increases3(my_input)))
