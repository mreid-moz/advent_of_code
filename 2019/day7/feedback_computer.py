import itertools

def pm(msg):
  print(msg)
  #pass

class Program:
  def __init__(self, program, label):
    self.halt = False
    self.program = program
    self.label = label
    self.offset = 0
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

    pm("{} Instruction {} at offset {}".format(self.label, opcode, self.offset))
    if opcode == 99:
      pm("  Halt")
      self.halt = True
      return False

    pos1 = self.program[self.offset + 1]
    param1 = self.get_param(mode1, pos1)

    if opcode == 3: # input
      pm("  Input")
      if len(self.input) > 0:
        pm("    From input list")
        input_value = self.input.pop(0)
      elif self.input_source is not None:
        # use input_source
        pm("    From input source")
        # If we need input, but don't have any, temporarily yield.
        if len(self.input_source.output) == 0:
          return False
        input_value = self.input_source.output.pop()
      else:
        pm("Trying to read input but there is none")
        self.halt = True
        return False


      pm("      Found input of '{}'".format(input_value))

      self.program[pos1] = input_value
      self.offset += 2
      return True

    if opcode == 4: # output
      pm("  Output")
      self.output.append(param1)
      self.offset += 2
      return True

    pos2 = self.program[self.offset + 2]
    param2 = self.get_param(mode2, pos2)

    if opcode == 5: # jump-if-true
      pm("  Jump if true: {} -> {}".format(param1, param2))
      if param1 != 0:
        self.offset = param2
      else:
        self.offset += 3
      return True

    if opcode == 6: # jump-if-false
      pm("  Jump if false")
      if param1 == 0:
        self.offset = param2
      else:
        self.offset += 3
      return True

    pos3 = self.program[self.offset + 3]

    if opcode == 1: # add
      pm("  Add {} + {} -> {}".format(param1, param2, pos3))
      self.program[pos3] = param1 + param2
    elif opcode == 2: # multiply
      pm("  Multiply")
      self.program[pos3] = param1 * param2
    elif opcode == 7: # less than
      pm("  Less than")
      self.program[pos3] = 1 if param1 < param2 else 0
    elif opcode == 8: # equals
      pm("  Equals")
      self.program[pos3] = 1 if param1 == param2 else 0
    else:
      pm("Unknown opcode: {}".format(opcode))
      self.halt = True
      return False

    self.offset += 4
    return True

  def get_param(self, mode, pos):
    if mode == 0:
      param = self.program[pos]
    elif mode == 1:
      param = pos
    else:
      pm("don't understand mode {}".format(mode))
      param = None
    return param

  def run_program(self):
    offset = 0
    while not self.halt and self.step():
      pass

def test_one(arr, expected):
  p = Program(arr)
  p.run_program()
  pm("{} -> {}".format(arr, p.program))
  assert(p.program == expected)

def test_one_output(arr, input, expected_output):
  p = Program(arr)
  p.set_input(input)
  p.run_program()
  actual_output = p.get_output()[-1]
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
  program = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
  assert(try_feedback([9,8,7,6,5], program) == 139629729)

  program = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
             -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
             53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
  assert(try_feedback([9,7,8,5,6], program) == 18216)
#
  #program = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
  #assert(try_iteration([1,0,4,3,2], program) == 65210)
  #m, mi = maximize([0,1,2,3,4], program)
  #assert(m == 65210)

  pm("All tests pass.")

test()

with open("input") as fin:
  line = fin.readline()
  original_program = [int(s) for s in line.split(",")]

m, mi = maximize([5,6,7,8,9], original_program)
print("Maximum output is {} using inputs {}".format(m, mi))