import logging
import sys

from math import gcd

logging.basicConfig(level=logging.DEBUG)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [l.strip() for l in fin.readlines()]

target_time = int(my_input[0])


def closest_multiple(n, target):
  m = 1
  while n * m < target:
    m += 1
  logging.debug("Closest multiple of {} to {} is {}x{}={}".format(n, target, m, n, m*n))
  return n * m

buses = my_input[1].split(',')

closest_time = None
bus_num = None
for b in buses:
  if b == 'x':
    continue
  current_bus_num = int(b)
  bus_time = closest_multiple(current_bus_num, target_time)
  if closest_time is None or bus_time < closest_time:
    bus_num = current_bus_num
    closest_time = bus_time

time_delta = closest_time - target_time
bus_product = bus_num * time_delta
logging.info("Part 1: Bus {} leaves closest to {} (at {}), {} x {} = {}".format(
  bus_num, target_time, closest_time, bus_num, time_delta, bus_product))

def lcm(a, b):
    """Find the least common multiple"""
    return abs(a * b) // gcd(a, b)

letters = 'abcdefghijklmnopqrst'

equations = list()
num_equations = 0
for i, v in enumerate(buses):
  if v == 'x':
    continue
  num_equations += 1
  equations.append((i, int(v)))
  logging.debug("Equation {}: {}{} - {} = t".format(num_equations, v, letters[num_equations-1], i))

base = equations[0][1]
equation_offset = 1
m = 1
m_step = 1
last_match = base
last_match_length = 1
while True:
  c = base * m
  good = True
  if m % 1000000 == 0:
    logging.info("Checking multiple {} * {}. m_step is {}".format(m, base, m_step))
  current_match_length = 0
  for offset, val in equations[equation_offset:]:
    if (c + offset) % val != 0:
      good = False
      break
    else:
      current_match_length += 1
      if last_match is None:
        last_match = c
        last_match_length = current_match_length
      #TODO: fix this trash
      # elif current_match_length > last_match_length:
      #  base = c - last_match
      #  m = 2
      #  logging.debug("Setting step size to {}".format(base))
      #  last_match = c
      #  last_match_length = current_match_length
      logging.debug("Found a value {} ({} * {}) that is {} % {} and {} % {}".format(c, base, m, offset, val, c % base, base))

      #if val > m_step:
      #  m_step = val
  if good:
    logging.info("part 2: Timestamp was {}".format(c))
    break
  m += m_step
