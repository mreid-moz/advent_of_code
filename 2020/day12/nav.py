import logging

class Nav:
  rotation_map = {
    ('N', 'L'): 'W',
    ('E', 'L'): 'N',
    ('W', 'L'): 'S',
    ('S', 'L'): 'E',

    ('N', 'R'): 'E',
    ('E', 'R'): 'S',
    ('W', 'R'): 'N',
    ('S', 'R'): 'W',
  }

  def __init__(self):
    self.x = 0
    self.y = 0
    self.dir = 'E'

  def rotate(self, direction, amount):
    prev = self.dir
    increments = amount // 90
    for i in range(increments):
      self.dir = Nav.rotation_map[(self.dir, direction)]
    logging.debug("{}{} goes from {} to {}".format(direction, amount, prev, self.dir))


  def move(self, cmd):
    d = cmd[0]
    if d == 'F':
      d = self.dir
    magnitude = int(cmd[1:])

    if d == 'N': # ORTH
      self.y -= magnitude
    elif d == 'S': # OUTH
      self.y += magnitude
    elif d == 'E': # AST
      self.x += magnitude
    elif d == 'W': # EST
      self.x -= magnitude
    elif d == 'L': # EFT
      self.rotate(d, magnitude)
    elif d == 'R': # IGHT
      self.rotate(d, magnitude)

  def manhattan(self):
    return abs(self.x) + abs(self.y)

class WaypointNav(Nav):
  def __init__(self):
    self.x = 0
    self.y = 0
    self.waypoint_x = 10
    self.waypoint_y = 1

  def rotate90(self, direction):
    prev_x = self.waypoint_x
    prev_y = self.waypoint_y
    if direction == 'R': # clockwise
      self.waypoint_x = prev_y
      self.waypoint_y = -prev_x
    else: # counterclockwise
      self.waypoint_x = -prev_y
      self.waypoint_y = prev_x


  def rotate(self, direction, amount):
    prev_wx = self.waypoint_x
    prev_wy = self.waypoint_y
    increments = amount // 90
    for i in range(increments):
      self.rotate90(direction)
    logging.debug("{}{} goes from ({},{}) to ({},{})".format(direction, amount, prev_wx, prev_wy, self.waypoint_x, self.waypoint_y))

  def move(self, cmd):
    logging.debug("About to move {}. Position is ({}, {}), waypoint is at ({}, {})".format(
      cmd, self.x, self.y, self.waypoint_x, self.waypoint_y))
    d = cmd[0]
    magnitude = int(cmd[1:])

    if d == 'N': # ORTH
      self.waypoint_y += magnitude
    elif d == 'S': # OUTH
      self.waypoint_y -= magnitude
    elif d == 'E': # AST
      self.waypoint_x += magnitude
    elif d == 'W': # EST
      self.waypoint_x -= magnitude
    elif d == 'L': # EFT
      self.rotate(d, magnitude)
    elif d == 'R': # IGHT
      self.rotate(d, magnitude)
    elif d == 'F': # ORWARD
      self.x += magnitude * self.waypoint_x
      self.y += magnitude * self.waypoint_y

    logging.debug("After moving {}, position is ({}, {}), waypoint is at ({}, {})".format(
      cmd, self.x, self.y, self.waypoint_x, self.waypoint_y))