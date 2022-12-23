from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2022, day=22)

PART_ONE = False

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
  if PART_ONE:
    return wrap_part_one(current_position, new_position, direction)
  else:
    return wrap_part_two(current_position, new_position, direction)

def wrap_part_one(current_position, new_position, direction):
  cr, cc = current_position
  nr, nc = new_position
  if direction == 'East':
    # we have to go back to column 0 and look
    for i in range(cc):
      if the_map[cr][i] == '.':
        return direction, nr, i
      if the_map[cr][i] == '#':
        return direction, cr, cc
  elif direction == 'South':
    # we have to go back to row 0 and look
    for i in range(cr):
      if cc >= len(the_map[i]):
        continue

      if the_map[i][cc] == '.':
        return direction, i, cc
      if the_map[i][cc] == '#':
        return direction, cr, cc
  elif direction == 'West':
    # we hit zero, have to go to the end
    for i in range(len(the_map[nr]) - 1, -1, -1):
      if the_map[cr][i] == '.':
        return direction, cr, i
      if the_map[cr][i] == '#':
        return direction, cr, cc
  elif direction == 'North':
    # we hit the top, go to the end
    for i in range(len(the_map) -1, -1, -1):
      if cc >= len(the_map[i]):
        continue

      if the_map[i][cc] == '.':
        return direction, i, cc
      if the_map[i][cc] == '#':
        return direction, cr, cc
  logging.warning("Error: fell out the end of wrap()")

def wrap_part_two(current_position, new_position, direction):
  cr, cc = current_position
  nr, nc = new_position
  nd = direction

  if nr < 0:
    if nc >= 50 and nc < 100: # A (north) -> L (east)
      logging.debug(f"Moving north from A {cr},{cc} -> {nr},{nc}")
      nr = nc + 100 # maybe 101
      nc = 0
      nd = 'East'
      logging.debug("wrapped north of A")
      # 0,50 -> 151, 0
      # 0,75 -> 175,0
      # 0,100 -> 200,0
    elif nc >= 100: # B (north) -> M (north)
      logging.debug(f"Moving north from B {cr},{cc} -> {nr},{nc}")
      nc = nc - 100 # maybe 101
      nr = 200
      nd = 'North'
      # 0,100 -> 200, 0
      # 0,125 -> 200,25
      # 0,150 -> 200,50
  elif nr < 50 and nc >= 150: # C (east) -> H (west)
    logging.debug(f"Moving east from C {cr},{cc} -> {nr},{nc}")
    nr = 150 - nr
    nc = 100
    nd = 'West'
    # 0, 150 -> 150,100
    # 25, 150 -> 125, 100
    # 50, 150 -> 100,100
  elif nr == 49 and nc >= 100 and nc < 150: # D (south) -> G (west)
    logging.debug(f"Moving south from D {cr},{cc} -> {nr},{nc}")
    nr = nc - 50
    nc = 100
    nd = 'West'
    # 50, 101 -> 51, 100
    # 50, 125 -> 75, 100
    # 50, 150 -> 100, 100
  elif nr < 50 and nc < 50: # E (west) -> K (east)
    logging.debug(f"Moving west from E {cr},{cc} -> {nr},{nc}")
    nr = 150 - nr
    nc = 0
    nd = 'East'
    # 0, 50 -> 150, 0
    # 25, 50 -> 125, 0
    # 50, 50 -> 100, 0
  elif nr >= 50 and nr < 100 and nc < 50: # F (west) -> J (south)
    logging.debug(f"Moving west from F {cr},{cc} -> {nr},{nc}")
    nc = nr - 50
    nr = 100
    nd = 'South'
    # 50, 50 -> 100, 0
    # 75, 50 -> 100, 25
    # 99, 50 -> 100, 50
  elif nr >= 50 and nr < 100 and nc >= 100: # G (east) -> D (north)
    logging.debug(f"Moving east from G {cr},{cc} -> {nr},{nc}")
    nc = nr + 50
    nr = 50 # maybe 49?
    nd = 'North'
    # 50, 100 -> 49, 100
    # 75, 100 -> 50, 125
    # 100, 100 -> 50, 150
  elif nr >= 50 and nr < 150 and nc >= 100: # H (east) -> C (west)
    logging.debug(f"Moving east from H {cr},{cc} -> {nr},{nc}")
    nr = 150 - nr
    nc = 150
    nd = 'West'
    # 100, 100 -> 50,150
    # 125, 100 -> 25,150
    # 150, 100 -> 0,150
  elif nr >= 150 and nc >= 50 and nc < 100: # I (south) -> N (west)
    logging.debug(f"Moving south from I {cr},{cc} -> {nr},{nc}")
    nr = nc + 100
    nc = 50
    nd = 'West'
    # 150, 50 -> 149, 50
    # 150, 75 -> 175, 50
    # 150, 99 -> 199, 50
  elif nr < 100 and nc < 50: # J (north) -> F (east)
    logging.debug(f"Moving north from J {cr},{cc} -> {nr},{nc}")
    nr = nc + 50
    nc = 50
    nd = 'East'
    # 100, 0 -> 50, 50
    # 100, 25 -> 75, 50
    # 100, 50 -> 100, 50
  elif nr >= 100 and nr < 150 and nc < 0: # K (west) -> E (east)
    logging.debug(f"Moving west from K {cr},{cc} -> {nr},{nc}")
    nr = 150 - nr
    nc = 50
    nd = 'East'
    # 100, 0 -> 50, 50
    # 125, 0 -> 25, 50
    # 150, 0 -> 0, 50
  elif nr >= 150 and nc < 0: # L (west) -> A (south)
    logging.debug(f"Moving west from L {cr},{cc} -> {nr},{nc}")
    nc = nr - 100
    nr = 0
    nd = 'South'
    # 150, 0 -> 0, 50
    # 175, 0 -> 0, 75
    # 200, 0 -> 0, 100
  elif nr >= 200: # M (south) -> B (south)
    logging.debug(f"Moving south from M {cr},{cc} -> {nr},{nc}")
    nc += 100
    nr = 0
    nd = 'South'
    # 200, 0 -> 0, 100
    # 200, 25 -> 0, 125
    # 200, 50 -> 0, 150
  elif nr >= 150 and nc >= 50: # N (east) -> I (north)
    logging.debug(f"Moving east from N {cr},{cc} -> {nr},{nc}")
    nc = nr - 100
    nc = 150 # 149 maybe?
    nd = 'North'
    # 150, 50 -> 149, 50
    # 175, 50 -> 149, 75
    # 200, 50 -> 149, 100
  else:
    logging.warning(f"Don't know how to wrap from {cr},{cc} -> {nr},{nc}")

  if the_map[nr][nc] == '.':
    logging.debug("wrapped spot was free")
    return nd, nr, nc
  elif the_map[nr][nc] == '#':
    logging.debug("wrapped spot was blocked by a wall")
    return direction, cr, cc
  else:
    logging.warning(f"Wrapping problem from {cr},{cc} -> {nr},{nc}, wrapped spot was '{the_map[nr][nc]}'.")
  ## something went wrong.
  return nd, nr, nc

def password(row, column, facing):
  return 1000 * row + 4 * column + facing

current_direction = 'East'
#                  (row, col)
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
            wd, wr, wc = wrap(current_position, (row, col), current_direction)
            logging.debug(f"Tried to move from {current_position} to {row},{col} wrapped from {current_direction} to {wd} to {wr},{wc}.")
            current_position = (wr, wc)
            current_direction = wd
        else:
          wd, wr, wc = wrap(current_position, (row, col), current_direction)
          logging.debug(f"column {col} is out of bounds, wrapped from {current_direction} to {wd} to {wr},{wc}")
          current_position = (wr, wc)
          current_direction = wd
      else:
        wd, wr, wc = wrap(current_position, (row, col), current_direction)
        logging.debug(f"row {row} is out of bounds, wrapped from {current_direction} to {wd} to {wr},{wc}")
        current_position = (wr, wc)
        current_direction = wd


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
  if PART_ONE:
    p.answer_a = final_password
