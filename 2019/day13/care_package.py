import logging
import itertools
logging.basicConfig(level=logging.WARN)

def debug(msg):
  #print(msg)
  pass

class IntcodeComputer:
  extra_memory = 100000
  def __init__(self, program, label="Computron"):
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

tiles = {}
tiles[0] = ' ' # empty
tiles[1] = '█' # wall
tiles[2] = '░' # block
tiles[3] = '═' # paddle
tiles[4] = 'o' # ball

with open('input') as fin:
  program = fin.read().strip()

instructions = [int(s) for s in program.split(",")]

class Game:
  def __init__(self, control_program):
    self.original_program = control_program.program.copy()
    self.original_moves = control_program.input.copy()
    self.ball_x = 0
    self.paddle_x = 0
    self.reset()

  def run_game(self):
    self.control_program.run_program()
    self.process_output()
    while True:
      self.update_screen()
      logging.info("Moves: [{}]".format(",".join([str(m) for m in self.moves])))
      self.get_input()
      while self.control_program.step():
        pass
      self.process_output()

  def reset(self):
    self.control_program = IntcodeComputer(self.original_program.copy())
    self.control_program.set_input(self.original_moves.copy())
    self.score = 0
    self.screen = {}
    self.moves = []
    self.control_program.run_program()
    self.process_output()

  def update_screen(self):
    print("".join(['-']*80))
    print("Score: {}".format(self.score))
    for y in range(40):
      for x in range(41):
        print("{}".format(tiles[self.screen.get((x, y), 0)]), end="")
      print("")
    print("".join(['-']*80))

  def get_input(self):
    answer = input("left a, neutral s, right d. Move? ")
    move = None
    if answer == 'a':
      move = -1
    elif answer == 'd':
      move = 1
    elif answer == 's':
      move = 0
    elif answer == 'R':
      self.reset()
    elif answer == '':
      # Just pressed enter. Default to the smart thing.
      logging.info("Default move")
      if self.paddle_x < self.ball_x:
        move = 1
      elif self.paddle_x > self.ball_x:
        move = -1
      else:
        move = 0
    # TODO: add "Undo" stack
    else:
      logging.info("Ignoring unknown direction '{}'.".format(answer))
    if move is not None:
      self.moves.append(move)
      self.control_program.input.append(move)

  def process_output(self):
    while len(self.control_program.output) >= 3:
      x = self.control_program.output.pop(0)
      y = self.control_program.output.pop(0)
      tile_id = self.control_program.output.pop(0)
      if tile_id == 4:
        logging.debug("Found ball at ({}, {})".format(x, y))
        self.ball_x = x
      if tile_id == 3:
        logging.debug("Found paddle at ({}, {})".format(x, y))
        self.paddle_x = x
      if x == -1 and y == 0:
        self.score = tile_id
      else:
        self.screen[(x, y)] = tile_id

instructions[0] = 2
computron = IntcodeComputer(instructions)
computron.set_input([0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,0,
                     0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,-1,-1,-1,-1,1,1,1,1,-1,-1,-1,-1,0,1,1,1,1,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,1,1,1,1,1,1,0,-1,-1,-1,-1,-1,-1,0,1,1,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,1,1,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,1,1,1,1,1,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,0,0,1,1,0,0,1,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,1,1,1,1,0,0,1,0,0,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,-1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,0,-1,-1,-1,0,0,-1,-1,-1,-1,0,-1,1,1,1,1,-1,-1,-1,-1,1,1,1,0,0,0,0,1,1,0,-1,-1,0,-1,0,0,0,0,0,0,0,0,0,1,1,0,0,-1,0,-1,-1,-1,1,1,1,1,1,1,1,0,0,0,-1,-1,0,-1,-1,-1,-1,0,-1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,0,-1,0,-1,-1,-1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,-1,0,0,0,-1,-1,-1,-1,-1,-1,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,-1,-1,-1,-1,1,1,1,1,0,0,0,0,1,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,0,-1,-1,-1,0,-1,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,0,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,-1,-1,-1,-1,-1,-1,-1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,0,0,0,0,-1,0,0,0,0,-1,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                     1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,
                     0,0,0,-1,-1,-1,0,0,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,-1,0,-1,0,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,0,-1,-1,-1,-1,-1,0,1,1,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,-1,-1,-1,-1,-1,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0,1,1,1,-1,-1,-1,1,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,-1,1,-1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,0,1,1,-1,-1,-1,-1,-1,-1,1,0,1,1,1,1,1,1,-1,-1,-1,-1,-1,0,-1,0,1,1,1,1,-1,1,1,0,-1,-1,1,0,1,1,1,1,0,0,0,-1,-1,1,0,1,0,-1,-1,-1,-1,-1,
                     -1,-1,0,0,0,1,1,1,1,1,-1,-1,-1,-1,-1,-1,1,-1,0,-1,-1,-1,-1,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,-1,-1,-1,-1,-1,0,0,0,-1,0,-1,-1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,0,0,0,1,1,-1,-1,0,0,0,-1,-1,-1,-1,-1,0,0,1,0,1,1,1,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,-1,0,0,0,0,0,1,1,1,1,1,0,0,0,1,1,-1,-1,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
                     ])
game = Game(computron)
game.run_game()

#computron.run_program()
#game.process_output()
#game.update_screen()
#
# block_counter = 0
# while len(computron.output) > 0:
#   x = computron.output.pop(0)
#   y = computron.output.pop(0)
#   tile_id = computron.output.pop(0)
#   if tile_id == 2:
#     block_counter += 1
#
# print("Found {} blocks".format(block_counter))