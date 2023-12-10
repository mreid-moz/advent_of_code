import logging
logging.basicConfig(level=logging.INFO)

class Maze:
  def __init__(self, maze_string):
    self.maze_string = maze_string
    self.maze = self.parse_maze(maze_string)
    self.key_count = self.count_keys()

  def __str__(self):
    return self.maze_string

  def parse_maze(self, maze_string):
    maze = {}
    lines = maze_string.strip().split("\n")
    for y, line in enumerate(lines):
      for x, c in enumerate(line):
        logging.debug("Found {} at ({},{})".format(c, x, y))
        if c != '#': # Skip walls
          maze[(x, y)] = c
    return maze

  def count_keys(self):
    key_count = 0
    for (x, y), v in self.maze.items():
      if v != '.' and v.islower():
        logging.info("Found key {} at ({},{})".format(v, x, y))
        key_count += 1
    return key_count

class MazePosition:
  def __init__(self, x, y, distance, keys):
    self.x = x
    self.y = y
    self.distance = distance
    self.keys = keys

def maze2tree(maze):
  pass

def shortest(tree):
  pass

class TestCase:
  def __init__(self, shortest_path_length, maze):
    self.shortest_path_length = shortest_path_length
    self.maze_string = maze.strip()
    self.maze = Maze(self.maze_string)
    self.tree = maze2tree(self.maze)

test_cases = [
  TestCase(8, """
#########
#b.A.@.a#
#########
"""),
  TestCase(86, """
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################
"""),
  TestCase(132, """
########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################
"""),
  TestCase(136, """
#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################
"""),
  TestCase(81, """
########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################
"""),
]

def test():

  for t in test_cases:
    shortest_path = shortest(t.maze)
    logging.info("{}-key maze:\n{}".format(t.maze.key_count, t.maze))
    logging.info("Shortest path: {} (len {}) vs. expected length {}".format(shortest_path, -1, t.shortest_path_length))
    #assert(len(shortest_path == t.shortest_path_length))
  logging.info("All tests pass.")
  pass

test()

# with open('input') as fin:
#   maze_string = fin.read().strip()

# maze = Maze(maze_string)
#logging.info("{}-key maze:\n{}".format(maze.key_count, maze.maze_string))