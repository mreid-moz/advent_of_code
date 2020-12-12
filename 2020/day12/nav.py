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
