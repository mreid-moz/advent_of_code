from computer import IntcodeComputer
import logging
logging.basicConfig(level=logging.INFO)


with open('input') as fin:
  program = fin.read().strip()
instructions = [int(s) for s in program.split(",")]

def get_first_x(y, m):
  for x in range(y + 1):
    if m.get((x, y), 0) == 1:
      return x

def max_diagonal(y, m, max_x):
  if y < 5:
    return 0
  first_x = get_first_x(y, m)

  logging.debug("found first x in row {} at ({}, {})".format(y, first_x, y))
  for offset in range(max_x - first_x):
    if m.get((first_x + offset, y - offset), 0) != 1:
      break
  #offset -= 1
  logging.debug("  top right at ({}, {}) size {}".format(first_x + offset - 1, y - offset + 1, offset))
  return offset

def verify_square(bottom_y, m, size):
  first_x = get_first_x(bottom_y, m)

  logging.debug("found first x in row {} at ({}, {})".format(bottom_y, first_x, bottom_y))

  for x in range(first_x, first_x + size):
    for y in range(bottom_y, bottom_y - size, -1):
      if m.get((x, y), 0) != 1:
        logging.info("Square starting at ({},{}) was missing ({},{})".format(first_x, bottom_y, x, y))
        return False
  return True

map_viz = {
  0: '.',
  1: '#',
  2: '0'
}

def show_map(m, min_x=0, min_y=0):
  mx = -1
  my = -1
  for x, y in m.keys():
    if x > mx:
      mx = x
    if y > my:
      my = y

  for y in range(min_y, my + 1):
    print("{0:03d}: ".format(y), end="")
    for x in range(min_x, mx + 1):
      print(map_viz.get(m.get((x, y), 176), ' '), end="")
    print("")

m = {}
total_affected = 0
distance = 1700
target_square = 100
start_y = 1000

max_line = 0
max_square = 0

for y in range(start_y, distance):
  line_affected = 0
  stopped_short = False
  for x in range(int(y/2), distance):
    computron = IntcodeComputer(instructions.copy())
    computron.set_input([x, y])
    computron.run_program()
    o = computron.output[-1]
    #if o == 1:
    #  logging.info("Beam at ({},{}): {}".format(x, y, o))
    m[(x,y)] = o
    if o == 1:
      line_affected += 1
    elif line_affected > 0:
      # Stop looking after the last affected space.
      stopped_short = True
      break
  # we're at the end of a line
  total_affected += line_affected
  if line_affected > max_line or max_square >= target_square:
    max_line = line_affected
    max_square = max_diagonal(y, m, distance)
    if max_square >= target_square and verify_square(y, m, target_square):
      top_left_x = get_first_x(y, m)
      top_left_y = y - target_square + 1
      logging.info("found it on line {}, top left coord is ({},{})".format(y, top_left_x, top_left_y))
      m[(top_left_x,top_left_y)] = 2
      #show_map(m) #, start_y, int(start_y/2))
      break
  if not stopped_short:
    logging.warn("Our lines are not long enough at {}".format(y))
  #shortcut = get_shortcut(x, y)
  #if shortcut != line_affected:
  #  logging.warning("shortcut ({}) didn't match actual ({})".format(shortcut, line_affected))
  logging.info("Line {} had {}, max square {}".format(y, line_affected, max_square))

#print("{} affected points".format(total_affected))



#show_map(m)

#......................................................................................###############..................
#.......................................................................................###############.................
#........................................................................................###############................
#.........................................................................................###############...............
#..........................................................................................###############..............
#..........................................................................................################.............
#...........................................................................................################............
#............................................................................................#######OOOOOOOOO...........
#.............................................................................................######OOOOOOOOO#..........
#..............................................................................................#####OOOOOOOOO##.........
#...............................................................................................####OOOOOOOOO###........
#...............................................................................................####OOOOOOOOO####.......
#................................................................................................###OOOOOOOOO#####......
#.................................................................................................##OOOOOOOOO######.....
#..................................................................................................#OOOOOOOOO#######....
#...................................................................................................OOOOOOOOO########...