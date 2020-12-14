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
while True:
  c = base * m
  good = True
  if m % 1000000 == 0:
    logging.debug("Checking multiple {} * {}".format(m, base))
  for offset, val in equations[equation_offset:]:
    if (c + offset) % val != 0:
      good = False
      break
  if good:
    logging.info("part 2: Timestamp was {}".format(base * m))
    break
  m += 1

# Equation 1: 17a + 0 = t
# Equation 2: 13b + 2 = t
# Equation 3: 19c + 3 = t
# t = 3417
