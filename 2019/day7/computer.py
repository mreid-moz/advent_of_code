import itertools

def pm(msg):
  print(msg)
  #pass

class Program:
  def __init__(self, program):
    self.halt = False
    self.program = program
    self.offset = 0
    self.input = []
    self.output = []

  def set_input(self, v):
    self.input = v

  def get_output(self):
    return self.output

  def step(self):
    instr = self.program[self.offset]
    opcode = instr % 100
    mode1 = int(instr / 100) % 10
    mode2 = int(instr / 1000) % 10
    mode3 = int(instr / 10000) % 10

    if opcode == 99:
      self.halt = True
      return False

    pos1 = self.program[self.offset + 1]
    param1 = self.get_param(mode1, pos1)

    if opcode == 3: # input
      input_value = self.input.pop(0)
      self.program[pos1] = input_value
      self.offset += 2
      return True

    if opcode == 4: # output
      self.output.append(param1)
      self.offset += 2
      return True

    pos2 = self.program[self.offset + 2]
    param2 = self.get_param(mode2, pos2)

    if opcode == 5: # jump-if-true
      if param1 != 0:
        self.offset = param2
      else:
        self.offset += 3
      return True

    if opcode == 6: # jump-if-false
      if param1 == 0:
        self.offset = param2
      else:
        self.offset += 3
      return True

    pos3 = self.program[self.offset + 3]

    if opcode == 1: # add
      self.program[pos3] = param1 + param2
    elif opcode == 2: # multiply
      self.program[pos3] = param1 * param2
    elif opcode == 7: # less than
      self.program[pos3] = 1 if param1 < param2 else 0
    elif opcode == 8: # equals
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
    while not self.halt:
      self.step()

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
  a = Program(program.copy())
  b = Program(program.copy())
  c = Program(program.copy())
  d = Program(program.copy())
  e = Program(program.copy())

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

def maximize(inputs, program):
  current_max = None
  max_iteration = None
  for iteration in itertools.permutations(inputs):
    result = try_iteration(iteration, program)
    if current_max is None or result > current_max:
      current_max = result
      max_iteration = iteration
  return current_max, max_iteration

def test():
  program = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
  assert(try_iteration([4,3,2,1,0], program) == 43210)

  program = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
  assert(try_iteration([0,1,2,3,4], program) == 54321)

  program = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
  assert(try_iteration([1,0,4,3,2], program) == 65210)
  m, mi = maximize([0,1,2,3,4], program)
  assert(m == 65210)

  pm("All tests pass.")

#test()

with open("input") as fin:
  line = fin.readline()
  original_program = [int(s) for s in line.split(",")]

m, mi = maximize([0,1,2,3,4], original_program)
print("Maximum output is {} using inputs {}".format(m, mi))