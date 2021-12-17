import logging
import copy
import re
import sys
from collections import defaultdict
from functools import reduce

logging.basicConfig(level=logging.DEBUG)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [l.strip() for l in fin.readlines()]

#target area: x=241..275, y=-75..-49

target_x_min = 241
target_x_max = 275

target_y_min = -75
target_y_max = -49

def triangle(n):
  # 1+2+3+4+...+n
  if n <= 0:
    return 0
  return (n * (n+1))//2

def get_x_after(initial_velocity, num_steps):
  return triangle(initial_velocity) - triangle(initial_velocity - num_steps)