import logging
import re
import sys
from copy import deepcopy

logging.basicConfig(level=logging.INFO)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [list(l.strip()) for l in fin.readlines()]

def count_adjacent_seats(seats, row, col):
  adj_count = 0
  for r_offset in [-1, 0, 1]:
    for c_offset in [-1, 0, 1]:
      if r_offset == 0 and c_offset == 0:
        continue
      nr = row + r_offset
      nc = col + c_offset
      if nr < 0 or nc < 0 or nr >= len(seats) or nc >= len(seats[0]):
        continue

      v = seats[row+r_offset][col+c_offset]
      if v == '#':
        adj_count += 1
      logging.debug("From ({},{}), checking ({},{})".format(row, col, row+r_offset, col+c_offset))

  logging.debug("({}, {}) has {} adjacent seats".format(row, col, adj_count))
  return adj_count

def update_seats(seats):
  updated_seats = deepcopy(seats)
  update_count = 0
  for row in range(len(seats)):
    for col in range(len(seats[0])):
      if seats[row][col] == '.':
        continue
      adj_count = count_adjacent_seats(seats, row, col)
      if seats[row][col] == 'L' and adj_count == 0:
        updated_seats[row][col] = '#'
        update_count += 1
      elif seats[row][col] == '#' and adj_count >= 4:
        updated_seats[row][col] = 'L'
        update_count += 1
  return updated_seats, update_count

def print_seats(seats):
  for row in seats:
    print(" ".join(row))
  print()

def count_occupied(seats):
  c = 0
  for row in seats:
    for s in row:
      if s == '#':
        c += 1
  return c

round_count = 0
logging.debug("Initial config:")
#print_seats(my_input)
seats = my_input
for i in range(100):
  round_count += 1
  seats, update_count = update_seats(seats)
  logging.info("After {} rounds:".format(round_count))
  #print_seats(seats)
  if update_count == 0:
    logging.info("Part 1: After {} rounds, the seating didn't change. There were {} occupied seats".format(round_count, count_occupied(seats)))
    break