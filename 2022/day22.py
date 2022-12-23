from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2022, day=22)

TEST = False
# TEST = True

if TEST:
  lines = [
    "        ...#",
    "        .#..",
    "        #...",
    "        ....",
    "...#.......#",
    "........#...",
    "..#....#....",
    "..........#.",
    "        ...#....",
    "        .....#..",
    "        .#......",
    "        ......#.",
    "",
    "10R5L5R10L4R5L5",
  ]
else:
  lines = p.input_data.splitlines()

logging.debug(f"Found {len(lines)} lines")

initial_position = lines[0].index('.')
logging.debug(f"Start pos: row 0, col {initial_position}")

move_str = lines[-1]
moves = []
current_num = ''
for c in move_str:
    if ord(c) >= ord('0') and ord(c) <= ord('9'):
        current_num += c
    else:
        moves.append(int(current_num))
        current_num = ''
        moves.append(c)
if current_num != '':
    moves.append(int(current_num))

logging.debug(f"Moves: {moves}")

the_map = lines[:-2]

def turn(cdir, mdir):
    if mdir == 'L':
        # turn left
        if cdir == 'East':
            return 'North'
        if cdir == 'South':
            return 'East'
        if cdir == 'West':
            return 'South'
        if cdir == 'North':
            return 'West'
    else:
        # turn right
        if cdir == 'East':
            return 'South'
        if cdir == 'South':
            return 'West'
        if cdir == 'West':
            return 'North'
        if cdir == 'North':
            return 'East'

def get_next_position(position, direction):
    row, col = position
    rd = 1
    cd = 1
    if direction == 'East':
        cd = 1
        rd = 0
    elif direction == 'South':
        cd = 0
        rd = 1
    elif direction == 'West':
        cd = -1
        rd = 0
    elif direction == 'North':
        cd = 0
        rd = -1

    return (row + rd, col + cd)

def wrap(current_position, new_position, direction):
    cr, cc = current_position
    nr, nc = new_position
    if direction == 'East':
        # we have to go back to column 0 and look
        for i in range(cc):
            if the_map[cr][i] == '.':
                return nr, i
            if the_map[cr][i] == '#':
                return cr, cc
    elif direction == 'South':
        # we have to go back to row 0 and look
        for i in range(cr):
            if cc >= len(the_map[i]):
              continue

            if the_map[i][cc] == '.':
                return i, cc
            if the_map[i][cc] == '#':
                return cr, cc
    elif direction == 'West':
        # we hit zero, have to go to the end
        for i in range(len(the_map[nr]) - 1, -1, -1):
            if the_map[cr][i] == '.':
                return cr, i
            if the_map[cr][i] == '#':
                return cr, cc
    elif direction == 'North':
        # we hit the top, go to the end
        for i in range(len(the_map) -1, -1, -1):
            if cc >= len(the_map[i]):
              continue

            if the_map[i][cc] == '.':
                return i, cc
            if the_map[i][cc] == '#':
                return cr, cc
    logging.warning("Error: fell out the end of wrap()")

def password(row, column, facing):
  return 1000 * row + 4 * column + facing

current_direction = 'East'
#                   row, col
current_position = (0, initial_position)
for m in moves:
    if m in ['L', 'R']:
        # it's a turn
        new_direction = turn(current_direction, m)
        logging.debug(f"Turning {m} from {current_direction} to {new_direction}")
        current_direction = new_direction
    else:
        # it's a distance
        for x in range(m):
            row, col = get_next_position(current_position, current_direction)
            if row < len(the_map) and row >= 0:
                if col < len(the_map[row]) and col >= 0:
                    if the_map[row][col] == '.':
                        # yay, we can move to it.
                        logging.debug(f"Moved from {current_position} to {row},{col}.")
                        current_position = (row, col)
                    elif the_map[row][col] == '#':
                        logging.debug(f"Can't move from {current_position} to {row},{col} because it's a wall.")
                    elif the_map[row][col] == ' ':
                        wr, wc = wrap(current_position, (row, col), current_direction)
                        logging.debug(f"Tried to move from {current_position} to {row},{col} wrapped to the {current_direction} to {wr},{wc}.")
                        current_position = (wr, wc)
                else:
                    wr, wc = wrap(current_position, (row, col), current_direction)
                    logging.debug(f"column {col} is out of bounds, wrapped to the {current_direction} to {wr},{wc}")
                    current_position = (wr, wc)
            else:
                wr, wc = wrap(current_position, (row, col), current_direction)
                logging.debug(f"row {row} is out of bounds, wrapped to the {current_direction} to {wr},{wc}")
                current_position = (wr, wc)


final_row, final_col = current_position
facing_map = {}
facing_map['East'] = 0
facing_map['South'] = 1
facing_map['West'] = 2
facing_map['North'] = 3
final_facing = facing_map[current_direction]

final_password = password(final_row + 1, final_col + 1, final_facing)
logging.info(f"Password: {final_password}")

if not TEST:
  p.answer_a = final_password
