import logging
import itertools
logging.basicConfig(level=logging.DEBUG)

def debug(msg):
  #print(msg)
  pass

class IntcodeComputer:
  extra_memory = 100000
  def __init__(self, program, label):
    self.halt = False
    self.program = program + [0] * IntcodeComputer.extra_memory
    self.label = label
    self.offset = 0
    self.relative_base = 0
    self.input = []
    self.output = []
    self.input_source = None

  def set_input(self, v):
    self.input = v

  def set_input_source(self, p):
    self.input_source = p

  def get_output(self):
    return self.output

  def step(self):
    instr = self.program[self.offset]
    opcode = instr % 100
    mode1 = int(instr / 100) % 10
    mode2 = int(instr / 1000) % 10
    mode3 = int(instr / 10000) % 10

    debug("{} Instruction {} at offset {}".format(self.label, opcode, self.offset))
    if opcode == 99:
      debug("  Halt")
      self.halt = True
      return False

    pos1 = self.program[self.offset + 1]
    param1 = self.get_param(mode1, pos1)
    io_pos1 = pos1
    if mode1 == 2:
      io_pos1 += self.relative_base

    if opcode == 3: # input
      debug("  Input")
      if len(self.input) > 0:
        debug("    From input list")
        input_value = self.input.pop(0)
      elif self.input_source is not None:
        # use input_source
        debug("    From input source")
        # If we need input, but don't have any, temporarily yield.
        if len(self.input_source.output) == 0:
          return False
        input_value = self.input_source.output.pop()
      else:
        debug("Trying to read input but there is none")
        self.halt = True
        return False
      debug("      Found input of '{}', putting it at {}".format(input_value, io_pos1))

      self.program[io_pos1] = input_value
      self.offset += 2
      return True

    if opcode == 4: # output
      debug("  Output '{}'".format(param1))
      self.output.append(param1)
      self.offset += 2
      return True

    if opcode == 9: # relative base offset
      debug("  Relative Base offset by {}".format(param1))
      self.relative_base += param1
      self.offset += 2
      return True

    pos2 = self.program[self.offset + 2]
    param2 = self.get_param(mode2, pos2)

    if opcode == 5: # jump-if-true
      debug("  Jump if true: {} -> {}".format(param1, param2))
      if param1 != 0:
        self.offset = param2
      else:
        self.offset += 3
      return True

    if opcode == 6: # jump-if-false
      debug("  Jump if false")
      if param1 == 0:
        self.offset = param2
      else:
        self.offset += 3
      return True

    pos3 = self.get_pos(mode3, self.offset + 3)

    if opcode == 1: # add
      debug("  Add {} + {} -> {}".format(param1, param2, pos3))
      self.program[pos3] = param1 + param2
    elif opcode == 2: # multiply
      debug("  Multiply")
      self.program[pos3] = param1 * param2
    elif opcode == 7: # less than
      debug("  Less than")
      self.program[pos3] = 1 if param1 < param2 else 0
    elif opcode == 8: # equals
      debug("  Equals")
      self.program[pos3] = 1 if param1 == param2 else 0
    else:
      debug("Unknown opcode: {}".format(opcode))
      self.halt = True
      return False

    self.offset += 4
    return True

  def get_param(self, mode, pos):
    if mode == 0:
      param = self.program[pos]
    elif mode == 1:
      param = pos
    elif mode == 2:
      param = self.program[self.relative_base + pos]
    else:
      debug("don't understand mode {}".format(mode))
      param = None
    return param

  def get_pos(self, mode, pos):
    pos = self.program[pos]
    if mode == 2:
      pos += self.relative_base
    return pos

  def run_program(self):
    offset = 0
    while not self.halt and self.step():
      pass

class Robot:
  def __init__(self, control_program):
    self.direction = 'UP'
    self.control_program = control_program
    self.position = (0,0)
    self.paint_state = {}

  def move(self):
    x, y = self.position

    delta_x = 0
    delta_y = 0

    if self.direction == 'UP':
      delta_y = -1
    elif self.direction == 'LEFT':
      delta_x = -1
    elif self.direction == 'DOWN':
      delta_y = 1
    elif self.direction == 'RIGHT':
      delta_x = 1

    self.position = (x + delta_x, y + delta_y)
    return self.position

  def turn(self, direction):
    d_change = [{
      # Left turns
      'UP':    'LEFT',
      'LEFT':  'DOWN',
      'DOWN':  'RIGHT',
      'RIGHT': 'UP'
    }, {
      # Right turns
      'UP':    'RIGHT',
      'RIGHT': 'DOWN',
      'DOWN':  'LEFT',
      'LEFT':  'UP'
    }]

    prev_direction = self.direction
    self.direction = d_change[direction][prev_direction]
    logging.debug("Turning {}, from {} to {}".format(direction, prev_direction, self.direction))

  def paint_stuff(self, starting_paint_colour):
    current_paint_state = self.paint_state.get(self.position, starting_paint_colour)
    self.control_program.input.append(current_paint_state)
    while not self.control_program.halt:
      logging.debug("Stepping until there's output")
      while len(self.control_program.output) < 2:
        #logging.debug("Stepping")
        self.control_program.step()
        if self.control_program.halt:
          break
      if len(self.control_program.output) < 2:
        break
      colour = self.control_program.output.pop(0)
      direction = self.control_program.output.pop(0)
      logging.info("Processing output: painting {} then turning {}".format(colour, direction))
      self.paint_state[self.position] = colour
      self.turn(direction)
      new_position = self.move()
      self.control_program.input.append(self.paint_state.get(new_position, 0))
      logging.info("Moved to {}".format(new_position))



with open("input") as fin:
  line = fin.readline()
  original_program = [int(s) for s in line.split(",")]

#paint = IntcodeComputer(original_program.copy(), 'Hull Painting Robot')
#robot = Robot(paint)
#robot.paint_stuff(0)

#print("Robot has painted {} panels".format(len(robot.paint_state)))

paint = IntcodeComputer(original_program.copy(), 'Hull Painting Robot')
robot = Robot(paint)
robot.paint_stuff(1)

min_x = None
max_x = None
min_y = None
max_y = None
for pos in robot.paint_state.keys():
  x, y = pos
  if min_x is None or x < min_x:
    min_x = x
  if min_y is None or x < min_y:
    min_y = x
  if max_x is None or x > max_x:
    max_x = x
  if max_y is None or x > max_y:
    max_y = x

grid_x = max_x - min_x + 1
grid_y = max_y - min_y + 1

grid = [ [' '] * grid_y for i in range(grid_x) ]

def show(g):
  rows = len(g[0])
  cols = len(g)

  for y in range(rows):
    for x in range(cols):
      print(g[x][y], end="")
    print("")
  print("")

for pos, colour in robot.paint_state.items():
  x, y = pos
  logging.info("Painting {}, {} as {}".format(x, y, colour))
  grid[x][y] = '█' if colour == 0 else ' '

show(grid)

print("Robot has painted {} panels".format(len(robot.paint_state)))