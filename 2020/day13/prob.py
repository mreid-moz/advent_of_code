import logging
import sys

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