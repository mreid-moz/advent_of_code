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

path = {}
for row, line in enumerate(the_map):
  for col, val in enumerate(line):
    path[(row, col)] = the_map[row][col]

dchars = {
  'North': '^',
  'South': 'v',
  'East': '>',
  'West': '<',
}

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

# sorry, future me and/or any readers :(
# this is terrible and only works for my own input and not the test.
# Input was shaped like this, and letters correspond to code below.
#
#      ..^....^..
#      ..A....B..
#      <E......C>
#      .......D..
#      .......v..
#      .....
#      .....
#      <F.G>
#      .....
#      .....
# ..^.......
# ..J.......
# <K......H>
# ......I...
# ......v...
# .....
# .....
# <L.N>
# ..M..
# ..v..
def wrap_part_two(current_position, new_position, direction):
  cr, cc = current_position
  nr, nc = new_position
  nd = direction

  if nr < 0 and nc >= 50 and nc < 100: # A (north) -> L (east)
      logging.debug(f"Moving north from A {cr},{cc} -> {nr},{nc}")
      nr = nc + 100
      nc = 0
      nd = 'East'
      # 0,50 -> 150,0
      # 0,75 -> 175,0
      # 0,99 -> 199,0
  elif nr < 0 and nc >= 100: # B (north) -> M (north)
      logging.debug(f"Moving north from B {cr},{cc} -> {nr},{nc}")
      nc = nc - 100
      nr = 199
      nd = 'North'
      # 0,100 -> 199, 0
      # 0,125 -> 199,25
      # 0,149 -> 199,49
  elif nr < 50 and nc >= 150: # C (east) -> H (west)
    logging.debug(f"Moving east from C {cr},{cc} -> {nr},{nc}")
    nr = 149 - nr
    nc = 99
    nd = 'West'
    # 0, 149 -> 149,99
    # 25, 149 -> 125,99
    # 49, 149 -> 100,99
  elif nr == 50 and nc >= 100 and nc < 150 and direction == 'South': # D (south) -> G (west)
    logging.debug(f"Moving south from D {cr},{cc} -> {nr},{nc}")
    nr = nc - 50
    nc = 99
    nd = 'West'
    # 49, 100 -> 50, 99
    # 49, 125 -> 75, 99
    # 49, 149 -> 99, 99
  elif nr < 50 and nc < 50: # E (west) -> K (east)
    logging.debug(f"Moving west from E {cr},{cc} -> {nr},{nc}")
    nr = 149 - nr
    nc = 0
    nd = 'East'
    # 0, 50 -> 149, 0
    # 25, 50 -> 125, 0
    # 49, 50 -> 100, 0
  elif nr >= 50 and nr < 100 and nc < 50 and direction == 'West': # F (west) -> J (south)
    logging.debug(f"Moving west from F {cr},{cc} -> {nr},{nc}")
    nc = nr - 50
    nr = 100
    nd = 'South'
    # 50, 50 -> 100, 0
    # 75, 50 -> 100, 25
    # 99, 50 -> 100, 49
  elif nr >= 50 and nr < 100 and nc >= 100 and direction == 'East': # G (east) -> D (north)
    logging.debug(f"Moving east from G {cr},{cc} -> {nr},{nc}")
    nc = nr + 50
    nr = 49
    nd = 'North'
    # 50, 99 -> 49, 100
    # 75, 99 -> 49, 125
    # 99, 99 -> 49, 149
  elif nr >= 100 and nr < 150 and nc >= 100: # H (east) -> C (west)
    logging.debug(f"Moving east from H {cr},{cc} -> {nr},{nc}")
    nr = 149 - nr
    nc = 149
    nd = 'West'
    # 100, 99 -> 49,149
    # 125, 99 -> 25,149
    # 149, 99 -> 0,149
  elif nr >= 150 and nc >= 50 and nc < 100 and direction == 'South': # I (south) -> N (west)
    logging.debug(f"Moving south from I {cr},{cc} -> {nr},{nc}")
    nr = nc + 100
    nc = 49
    nd = 'West'
    # 149, 50 -> 150, 49
    # 149, 75 -> 175, 49
    # 149, 99 -> 199, 49
  elif nr < 100 and nc < 50 and direction == 'North': # J (north) -> F (east)
    logging.debug(f"Moving north from J {cr},{cc} -> {nr},{nc}")
    nr = nc + 50
    nc = 50
    nd = 'East'
    # 100, 0 -> 50, 50
    # 100, 25 -> 75, 50
    # 100, 49 -> 99, 50
  elif nr >= 100 and nr < 150 and nc < 0: # K (west) -> E (east)
    logging.debug(f"Moving west from K {cr},{cc} -> {nr},{nc}")
    nr = 149 - nr
    nc = 50
    nd = 'East'
    # 100, 0 -> 49, 50
    # 125, 0 -> 25, 50
    # 149, 0 -> 0, 50
  elif nr >= 150 and nr < 200 and nc < 0: # L (west) -> A (south)
    logging.debug(f"Moving west from L {cr},{cc} -> {nr},{nc}")
    nc = nr - 100
    nr = 0
    nd = 'South'
    # 150, 0 -> 0, 50
    # 175, 0 -> 0, 75
    # 199, 0 -> 0, 99
  elif nr >= 200: # M (south) -> B (south)
    logging.debug(f"Moving south from M {cr},{cc} -> {nr},{nc}")
    nc += 100
    nr = 0
    nd = 'South'
    # 199, 0 -> 0, 100
    # 199, 25 -> 0, 125
    # 199, 49 -> 0, 149
  elif nr >= 150 and nc >= 50 and direction == 'East': # N (east) -> I (north)
    logging.debug(f"Moving east from N {cr},{cc} -> {nr},{nc}")
    nc = nr - 100
    nr = 149
    nd = 'North'
    # 150, 49 -> 149, 50
    # 175, 49 -> 149, 75
    # 199, 49 -> 149, 99
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

def print_path(p, f=None):
  if f is None:
    for row, line in enumerate(the_map):
      for col, val in enumerate(line):
        print(p[(row, col)], end='')
      print('')
  else:
    with open(f, 'w') as fout:
      for row, line in enumerate(the_map):
        for col, val in enumerate(line):
          fout.write(p[(row, col)])
        fout.write('\n')
      fout.write('\n')


current_direction = 'East'
#                  (row, col)
current_position = (0, initial_position)

# tag each end of a wrap with a letter so we can see wtf is happening.
wrap_char = ord('A')

for m in moves:
  if m in ['L', 'R']:
    # it's a turn
    new_direction = turn(current_direction, m)
    logging.debug(f"Turning {m} from {current_direction} to {new_direction}")
    current_direction = new_direction
    path[current_position] = dchars[new_direction]
  else:
    # it's a distance
    logging.debug(f"Moving {m} {current_direction}")
    for x in range(m):
      row, col = get_next_position(current_position, current_direction)
      if row < len(the_map) and row >= 0:
        if col < len(the_map[row]) and col >= 0:
          if the_map[row][col] == '.':
            # yay, we can move to it.
            logging.debug(f"Moved from {current_position} to {row},{col}.")
            current_position = (row, col)
            if ord(path[(row,col)]) >= ord('A') and ord(path[(row,col)]) <= ord('z'):
              logging.debug(f'Not overwriting path crossover {path[(row,col)]} with boring direction {dchars[current_direction]}')
            else:
              path[(row,col)] = dchars[current_direction]
          elif the_map[row][col] == '#':
            logging.debug(f"Can't move from {current_position} to {row},{col} because it's a wall.")
            break
          elif the_map[row][col] == ' ':
            wd, wr, wc = wrap(current_position, (row, col), current_direction)
            logging.debug(f"_{chr(wrap_char)}_ Tried to move from {current_position} to {row},{col} wrapped from {current_direction} to {wd} to {wr},{wc}.")
            if (wr, wc) != current_position:
              path[current_position] = chr(wrap_char)
              current_position = (wr, wc)
              current_direction = wd
              path[current_position] = chr(wrap_char)
              wrap_char += 1
            else:
              logging.debug(f"Couldn't move after wrap (1)")
        else:
          wd, wr, wc = wrap(current_position, (row, col), current_direction)
          logging.debug(f"_{chr(wrap_char)}_ column {col} is out of bounds, wrapped from {current_direction} to {wd} to {wr},{wc}")
          if (wr, wc) != current_position:
            path[current_position] = chr(wrap_char)
            current_position = (wr, wc)
            current_direction = wd
            path[current_position] = chr(wrap_char)
            wrap_char += 1
          else:
            logging.debug(f"Couldn't move after wrap (2)")
      else:
        wd, wr, wc = wrap(current_position, (row, col), current_direction)
        logging.debug(f"_{chr(wrap_char)}_ row {row} is out of bounds, wrapped from {current_direction} to {wd} to {wr},{wc}")
        if (wr, wc) != current_position:
          path[current_position] = chr(wrap_char)
          current_position = (wr, wc)
          current_direction = wd
          path[current_position] = chr(wrap_char)
          wrap_char += 1
        else:
          logging.debug(f"Couldn't move after wrap (3)")
      if wrap_char >= 122:
        wrap_char = ord('A')
        # print_path(path)
        # print_path(path, f='d22path.log')
        # sys.exit(-1)

final_row, final_col = current_position
facing_map = {
  'East': 0,
  'South': 1,
  'West': 2,
  'North': 3,
}
final_facing = facing_map[current_direction]

final_password = password(final_row + 1, final_col + 1, final_facing)

logging.info("Final path:")
print_path(path)
print_path(path, f='d22path.log')

logging.info(f"Password: {final_password}")

if not TEST:
  if PART_ONE:
    p.answer_a = final_password
  else:
    p.answer_b = final_password