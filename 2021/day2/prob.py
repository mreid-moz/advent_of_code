import logging
import re
import sys

logging.basicConfig(level=logging.INFO)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [l.strip() for l in fin.readlines()]

horizontal_position = 0
depth = 0

for move in my_input:
  direction, distance = move.split(' ')
  distance = int(distance)
  if direction == 'forward':
    horizontal_position += distance
  elif direction == 'down':
    depth += distance
  elif direction == 'up':
    depth -= distance
  else:
    logging.warn("Don't understand move: {}".format(move))

logging.info("Part 1: {}".format(horizontal_position * depth))

horizontal_position = 0
depth = 0
aim = 0

for move in my_input:
  direction, distance = move.split(' ')
  distance = int(distance)
  if direction == 'forward':
    horizontal_position += distance
    depth += aim * distance
  elif direction == 'down':
    aim += distance
  elif direction == 'up':
    aim -= distance
  else:
    logging.warn("Don't understand move: {}".format(move))

logging.info("Part 2: {}".format(horizontal_position * depth))