import itertools

def debug(msg):
  #print(msg)
  pass

class Program:
  extra_memory = 100000
  def __init__(self, program, label):
    self.halt = False
    self.program = program + [0] * Program.extra_memory
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

def test_one(arr, expected):
  p = Program(arr, 'Test')
  p.run_program()
  debug("{} -> {}".format(arr, p.program))
  assert(p.program == expected)

def test_one_output(arr, input, expected_output):
  p = Program(arr, 'Test')
  p.set_input(input)
  p.run_program()
  actual_output = p.get_output()
  debug("Actual: {}, expected: {}".format(actual_output, expected_output))
  assert(actual_output == expected_output)

def try_iteration(inputs, program):
  a = Program(program.copy(), 'A')
  b = Program(program.copy(), 'B')
  c = Program(program.copy(), 'C')
  d = Program(program.copy(), 'D')
  e = Program(program.copy(), 'E')

  a.set_input([inputs[0], 0])
  a.run_program()
  b.set_input([inputs[1], a.get_output()[-1]])
  b.run_program()
  c.set_input([inputs[2], b.get_output()[-1]])
  c.run_program()
  d.set_input([inputs[3], c.get_output()[-1]])
  d.run_program()
  e.set_input([inputs[4], d.get_output()[-1]])
  e.run_program()
  return e.get_output()[-1]

def try_feedback(inputs, program):
  a = Program(program.copy(), 'A')
  b = Program(program.copy(), 'B')
  c = Program(program.copy(), 'C')
  d = Program(program.copy(), 'D')
  e = Program(program.copy(), 'E')

  a.set_input([inputs[0], 0])
  a.set_input_source(e)

  b.set_input([inputs[1]])
  b.set_input_source(a)

  c.set_input([inputs[2]])
  c.set_input_source(b)

  d.set_input([inputs[3]])
  d.set_input_source(c)

  e.set_input([inputs[4]])
  e.set_input_source(d)

  while True:
    a.run_program()
    b.run_program()
    c.run_program()
    d.run_program()
    e.run_program()
    # Check if they've all halted
    if False not in set([a.halt, b.halt, c.halt, d.halt, e.halt]):
      break
  return e.get_output()[-1]

def maximize(inputs, program):
  current_max = None
  max_iteration = None
  for iteration in itertools.permutations(inputs):
    result = try_feedback(iteration, program)
    if current_max is None or result > current_max:
      current_max = result
      max_iteration = iteration
  return current_max, max_iteration

def test():
  program = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
  test_one_output(program, [], program)

  program = [1102,34915192,34915192,7,4,7,99,0]
  test_one_output(program, [], [1219070632396864])

  program = [104,1125899906842624,99]
  test_one_output(program, [], [1125899906842624])

  program = [203,3,104,0,99]
  test_one_output(program, [123], [123])

  program = [109,5,203,0,104,0,99]
  test_one_output(program, [111], [111])

  print("All tests pass.")

test()

with open("input") as fin:
  line = fin.readline()
  original_program = [int(s) for s in line.split(",")]

print("running test")
boost = Program(original_program.copy(), 'BOOST')
boost.set_input([1])
boost.run_program()
print("Output: {}".format(boost.get_output()))

print("Running for reals")
boost = Program(original_program.copy(), 'BOOST')
boost.set_input([2])
boost.run_program()
print("Output: {}".format(boost.get_output()))