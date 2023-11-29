from computer import IntcodeComputer
import logging
logging.basicConfig(level=logging.INFO)

with open('input') as fin:
  program = fin.read().strip()
instructions = [int(s) for s in program.split(",")]

def to_ascii(stringy):
  return [ord(c) for c in stringy]

# Part 2:
instructions[0] = 2

scaffold_routine = to_ascii("A,B,B,A,C,A,C,A,C,B") + [10] + \
                   to_ascii("L,6,R,12,R,8") + [10] + \
                   to_ascii("R,8,R,12,L,12") + [10] + \
                   to_ascii("R,12,L,12,L,4,L,4") + [10] + \
                   to_ascii("n") + [10]

computron = IntcodeComputer(instructions)
computron.set_input(scaffold_routine)
computron.run_program()

def extract_map(computron):
  scaffold_map = {}
  # Display computron's output
  row = 0
  col = 0
  for c in computron.output:
    logging.debug("Found an ouput of {}".format(c))
    #print(chr(c), end="")
    if c == 10:
      row += 1
      col = 0
    else:
      logging.info("Setting ({},{}) to {}".format(col, row, c))
      scaffold_map[(col, row)] = c
      col += 1
  return scaffold_map

def show_map(m):
  mx = -1
  my = -1
  for x, y in m.keys():
    if x > mx:
      mx = x
    if y > my:
      my = y

  for y in range(my+1):
    for x in range(mx+1):
      print(chr(m.get((x, y), 176)), end="")
    print("")

def is_scaffold(x, y, m):
  return m.get((x, y), -1) == 35

def is_intersection(x, y, m):
  if is_scaffold(x, y, m) and is_scaffold(x-1, y, m) and is_scaffold(x+1, y, m) and is_scaffold(x, y-1, m) and is_scaffold(x, y+1, m):
      return True
  return False

def get_intersections(m):
  intersections = []
  for x, y in m.keys():
    if is_intersection(x, y, m):
      logging.info("Found an intersection at ({},{}) = {}".format(x, y, x * y))
      intersections.append((x, y))
    else:
      logging.debug("Found a non-intersection at ({},{})".format(x, y))
  return intersections

def get_alignment_params(intersections):
  total = 0
  for x, y in intersections:
    total += x * y
  return total

def parse_map(s):
  m = {}
  for r, line in enumerate(s.strip().split("\n")):
    for c, v in enumerate(line):
      m[(c, r)] = ord(v)
  return m


test_pattern = """
..#..........
..#..........
#######...###
#.#...#...#.#
#############
..#...#...#..
..#####...^..
""".strip()

m = parse_map(test_pattern)
show_map(m)
intersections = get_intersections(m)
ap = get_alignment_params(intersections)
print("Example: {}".format(ap))
assert(ap == 76)


# scaffold_map = extract_map(computron)
# show_map(scaffold_map)
# intersections = get_intersections(scaffold_map)
# for i in intersections:
#   scaffold_map[i] = ord('O')
# show_map(scaffold_map)

# print("sum of alignment_parameters: {}".format(get_alignment_params(intersections)))

# ..............DDDDD................................
# ..............D...D................................
# ....DDDDDDDDDDDDD.D................................
# ....D.........D.D.D................................
# DDDDDDDDDDDDD.DDDDDDD..............................
# D...D.......D...D.D.D..............................
# D...D.......D...D.D.D.....................DDDDDDDDD
# D...D.......D...D.D.D.....................D.......D
# DDDDD.......D...D.D.D.....................D.......D
# ............D...D.D.D.....................D.......D
# ....DDDDDDDDDDDDD.D.D.....................D.......D
# ....D.......D.....D.D.....................D.......D
# ....D.DDDDDDDDDDDDD.D.....................D.......D
# ....D.D.....D.......D.....................D.......D
# ....D.D.....D.....DDDDDDDDDDDDD.......DDDDDDDDDDDDD
# ....D.D.....D.....D.D.........D.......D...D........
# ....D.D.....DDDDDDDDD.........D.......D...D........
# ....D.D...........D...........D.......D...D........
# ....D.D.DDDDDDDDD.D...........D.......D...DDDDDD^..
# ....D.D.D.......D.D...........D.......D............
# ....D.DDDDDDDDDDDDD...........D.......D............
# ....D...D.......D.............D.......D............
# ....DDDDD.......D.............D.......D............
# ................D.............D.......D............
# ................D.............D.......D............
# ................D.............D.......D............
# ................D.............DDDDDDDDD............
# ................D..................................
# ................D..................................
# ................D..................................
# ................DDDDDDDDDDDDD......................



# L,6,R,12,R,8,R,8,R,12,L,12,R,8,R,12,L,12,L,6,R,12,R,8,R,12,L,12,L,4,L,4,L,6,R,12,R,8,R,12,L,12,L,4,L,4,L,6,R,12,R,8,R,12,L,12,L,4,L,4,R,8,R,12,L,12

# A=L,6,R,12,R,8
# B=R,8,R,12,L,12
# C=R,12,L,12,L,4,L,4
# A,B,B,A,C,A,C,A,C,B


print(computron.output[-1])
