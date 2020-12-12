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

def valid_position(seats, row, col):
  return row >= 0 and col >= 0 and row < len(seats) and col < len(seats[0])

def count_adjacent_seats(seats, row, col):
  adj_count = 0
  for r_offset in [-1, 0, 1]:
    for c_offset in [-1, 0, 1]:
      if r_offset == 0 and c_offset == 0:
        continue
      nr = row + r_offset
      nc = col + c_offset
      if not valid_position(seats, nr, nc):
        continue

      v = seats[row+r_offset][col+c_offset]
      if v == '#':
        adj_count += 1
      logging.debug("From ({},{}), checking ({},{})".format(row, col, row+r_offset, col+c_offset))

  logging.debug("({}, {}) has {} adjacent seats".format(row, col, adj_count))
  return adj_count


def count_visible_seats(seats, row, col):
  vis_count = 0
  for slope_y in [-1, 0, 1]:
    for slope_x in [-1, 0, 1]:
      if slope_y == 0 and slope_x == 0:
        continue

      logging.debug("Checking slope ({}, {}) from ({}, {})".format(slope_y, slope_x, row, col))
      p_row = row + slope_y
      p_col = col + slope_x
      last_seat = None
      while valid_position(seats, p_row, p_col):
        last_seat = seats[p_row][p_col]
        logging.debug("Checking {}, {} -> {}".format(p_row, p_col, last_seat))
        if last_seat in ['#', 'L']:
          break
        p_row += slope_y
        p_col += slope_x

      if last_seat == '#':
        logging.debug("it was visible")
        vis_count += 1

  logging.debug("({}, {}) has {} visible seats".format(row, col, vis_count))
  return vis_count

def update_seats(seats, visible=False):
  max_seats = 4
  if visible:
    max_seats = 5
  updated_seats = deepcopy(seats)
  update_count = 0
  for row in range(len(seats)):
    for col in range(len(seats[0])):
      if seats[row][col] == '.':
        continue
      seat_count = 0
      if visible:
        seat_count = count_visible_seats(seats, row, col)
      else:
        seat_count = count_adjacent_seats(seats, row, col)
      if seats[row][col] == 'L' and seat_count == 0:
        updated_seats[row][col] = '#'
        update_count += 1
      elif seats[row][col] == '#' and seat_count >= max_seats:
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
seats = deepcopy(my_input)
for i in range(100):
  round_count += 1
  seats, update_count = update_seats(seats)
  logging.info("After {} rounds:".format(round_count))
  #print_seats(seats)
  if update_count == 0:
    logging.info("Part 1: After {} rounds, the seating didn't change. There were {} occupied seats".format(round_count, count_occupied(seats)))
    break

def test():
  t1 = [
   ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
   ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
   ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
   ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
   ['.', '.', '.', 'L', '.', '.', '.', '.', '.'],
   ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
   ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
   ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
   ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
  ]
  logging.debug("t1: {} should be 0".format(count_visible_seats(t1, 4, 3)))

  t2 = [
   ['.', '.', '.', '.', '.', '.', '.', '#', '.'],
   ['.', '.', '.', '#', '.', '.', '.', '.', '.'],
   ['.', '#', '.', '.', '.', '.', '.', '.', '.'],
   ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
   ['.', '.', '#', 'L', '.', '.', '.', '.', '#'],
   ['.', '.', '.', '.', '#', '.', '.', '.', '.'],
   ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
   ['#', '.', '.', '.', '.', '.', '.', '.', '.'],
   ['.', '.', '.', '#', '.', '.', '.', '.', '.'],
  ]
  logging.debug("t2: {} should be 8".format(count_visible_seats(t2, 4, 3)))

  t3 = [
   ['.', '#', '#', '.', '#', '#', '.'],
   ['#', '.', '#', '.', '#', '.', '#'],
   ['#', '#', '.', '.', '.', '#', '#'],
   ['.', '.', '.', 'L', '.', '.', '.'],
   ['#', '#', '.', '.', '.', '#', '#'],
   ['#', '.', '#', '.', '#', '.', '#'],
   ['.', '#', '#', '.', '#', '#', '.'],
  ]
  logging.debug("t3: {} should be 0".format(count_visible_seats(t3, 3, 3)))


#test()

round_count = 0
seats = deepcopy(my_input)
for i in range(200):
  round_count += 1
  seats, update_count = update_seats(seats, visible=True)
  logging.info("After {} rounds:".format(round_count))
  #print_seats(seats)
  if update_count == 0:
    logging.info("Part 2: After {} rounds, the seating didn't change. There were {} occupied seats".format(round_count, count_occupied(seats)))
    break
