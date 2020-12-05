import logging
import itertools

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

    logging.debug("{} Instruction {} at offset {}".format(self.label, opcode, self.offset))
    if opcode == 99:
      logging.debug("  Halt")
      self.halt = True
      return False

    pos1 = self.program[self.offset + 1]
    param1 = self.get_param(mode1, pos1)
    io_pos1 = pos1
    if mode1 == 2:
      io_pos1 += self.relative_base

    if opcode == 3: # input
      logging.debug("  Input")
      if len(self.input) > 0:
        logging.debug("    From input list")
        input_value = self.input.pop(0)
      elif self.input_source is not None:
        # use input_source
        logging.debug("    From input source")
        # If we need input, but don't have any, temporarily yield.
        if len(self.input_source.output) == 0:
          return False
        input_value = self.input_source.output.pop()
      else:
        logging.debug("Trying to read input but there is none")
        self.halt = True
        return False
      logging.debug("      Found input of '{}', putting it at {}".format(input_value, io_pos1))

      self.program[io_pos1] = input_value
      self.offset += 2
      return True

    if opcode == 4: # output
      logging.debug("  Output '{}'".format(param1))
      self.output.append(param1)
      self.offset += 2
      return True

    if opcode == 9: # relative base offset
      logging.debug("  Relative Base offset by {}".format(param1))
      self.relative_base += param1
      self.offset += 2
      return True

    pos2 = self.program[self.offset + 2]
    param2 = self.get_param(mode2, pos2)

    if opcode == 5: # jump-if-true
      logging.debug("  Jump if true: {} -> {}".format(param1, param2))
      if param1 != 0:
        self.offset = param2
      else:
        self.offset += 3
      return True

    if opcode == 6: # jump-if-false
      logging.debug("  Jump if false")
      if param1 == 0:
        self.offset = param2
      else:
        self.offset += 3
      return True

    pos3 = self.get_pos(mode3, self.offset + 3)

    if opcode == 1: # add
      logging.debug("  Add {} + {} -> {}".format(param1, param2, pos3))
      self.program[pos3] = param1 + param2
    elif opcode == 2: # multiply
      logging.debug("  Multiply")
      self.program[pos3] = param1 * param2
    elif opcode == 7: # less than
      logging.debug("  Less than")
      self.program[pos3] = 1 if param1 < param2 else 0
    elif opcode == 8: # equals
      logging.debug("  Equals")
      self.program[pos3] = 1 if param1 == param2 else 0
    else:
      logging.debug("Unknown opcode: {}".format(opcode))
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
      logging.debug("don't understand mode {}".format(mode))
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