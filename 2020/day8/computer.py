import logging

class NormalTermination(Exception):
  pass

class AbormalTermination(Exception):
  pass

class Instruction:
  def __init__(self, line):
    opcode, arg = line.split(" ")
    self.opcode = opcode
    self.arg = int(arg)
    self.visits = 0


class Computer:
  def __init__(self, program):
    self.accumulator = 0
    self.program_counter = 0
    self.instructions = list()
    for line in program:
      self.instructions.append(Instruction(line))

  def print_instructions(self):
    for i in self.instructions:
      print("{}  {}  (processed {} times)".format(i.opcode, i.arg, i.visits))

  def get_current_instruction(self):
    return self.instructions[self.program_counter]

  def step(self):
    if self.program_counter == len(self.instructions):
      raise NormalTermination("OK")
    elif self.program_counter > len(self.instructions):
      raise AbnormalTermination("Error: program_counter {} vs. {} instructions.".format(
        self.program_counter, len(self.instructions)))
    instruction = self.get_current_instruction()

    ####### maybe bogus! #########
    if instruction.visits > 2:
      raise AbnormalTermination("Infinite loop")
    ##############################

    jump_value = 1
    # process the instruction
    logging.debug("processing instruction {}({}) on accumulator={}".format(
      instruction.opcode, instruction.arg, self.accumulator))
    if instruction.opcode == 'nop': # No-op
      pass
    elif instruction.opcode == 'acc': # accumulate
      self.accumulator += instruction.arg
      logging.debug("accumulator changed to {}".format(self.accumulator))
    elif instruction.opcode == 'jmp': # jump
      logging.debug("jumping from {} to {}".format(
        self.program_counter, self.program_counter + instruction.arg))
      jump_value = instruction.arg
      if jump_value == 0:
        raise AbnormalTermination("Tried to jump zero :(")
    self.program_counter += jump_value

    instruction.visits += 1

  def run(self):
    try:
      while True:
        self.step()
    except NormalTermination:
      pass
