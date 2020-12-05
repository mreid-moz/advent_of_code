#--- Part Two ---
#
#The air conditioner comes online! Its cold air feels good for a while, but then the TEST alarms start to go off. Since the air conditioner can't vent its heat anywhere but back into the spacecraft, it's actually making the air inside the ship warmer.
#
#Instead, you'll need to use the TEST to extend the thermal radiators. Fortunately, the diagnostic program (your puzzle input) is already equipped for this. Unfortunately, your Intcode computer is not.
#
#Your computer is only missing a few opcodes:
#
#    Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
#    Opcode 6 is jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
#    Opcode 7 is less than: if the first parameter is less than the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
#    Opcode 8 is equals: if the first parameter is equal to the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
#
#Like all instructions, these instructions need to support parameter modes as described above.
#
#Normally, after an instruction is finished, the instruction pointer increases by the number of values in that instruction. However, if the instruction modifies the instruction pointer, that value is used and the instruction pointer is not automatically increased.
#
#For example, here are several programs that take one input, compare it to the value 8, and then produce one output:
#
#    3,9,8,9,10,9,4,9,99,-1,8 - Using position mode, consider whether the input is equal to 8; output 1 (if it is) or 0 (if it is not).
#    3,9,7,9,10,9,4,9,99,-1,8 - Using position mode, consider whether the input is less than 8; output 1 (if it is) or 0 (if it is not).
#    3,3,1108,-1,8,3,4,3,99 - Using immediate mode, consider whether the input is equal to 8; output 1 (if it is) or 0 (if it is not).
#    3,3,1107,-1,8,3,4,3,99 - Using immediate mode, consider whether the input is less than 8; output 1 (if it is) or 0 (if it is not).
#
#Here are some jump tests that take an input, then output 0 if the input was zero or 1 if the input was non-zero:
#
#    3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9 (using position mode)
#    3,3,1105,-1,9,1101,0,0,12,4,12,99,1 (using immediate mode)
#
#Here's a larger example:
#
#3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
#1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
#999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99
#
#The above example program uses an input instruction to ask for a single number. The program will then output 999 if the input value is below 8, output 1000 if the input value is equal to 8, or output 1001 if the input value is greater than 8.
#
#This time, when the TEST diagnostic program runs its input instruction to get the ID of the system to test, provide it 5, the ID for the ship's thermal radiator controller. This diagnostic test suite only outputs one number, the diagnostic code.
#
#What is the diagnostic code for system ID 5?

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

    #pm("Modes: {}, {}, {}".format(mode1, mode2, mode3))

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

def test():
  test_one([1,0,0,0,99], [2,0,0,0,99])
  test_one([2,3,0,3,99], [2,3,0,6,99])
  test_one([2,4,4,5,99,0], [2,4,4,5,99,9801])
  test_one([1,1,1,4,99,5,6,0,99], [30,1,1,4,2,5,6,0,99])
  test_one([1002,4,3,4,33], [1002,4,3,4,99])
  test_one([1101,100,-1,4,0], [1101,100,-1,4,99])

  test_one_output([3,9,8,9,10,9,4,9,99,-1,8], [8], 1)
  test_one_output([3,9,8,9,10,9,4,9,99,-1,8], [7], 0)

  test_one_output([3,9,7,9,10,9,4,9,99,-1,8], [5], 1)
  test_one_output([3,9,7,9,10,9,4,9,99,-1,8], [10], 0)

  test_one_output([3,3,1107,-1,8,3,4,3,99], [5], 1)
  test_one_output([3,3,1107,-1,8,3,4,3,99], [10], 0)

  test_one_output([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], [0], 0)
  test_one_output([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], [1], 1)
  test_one_output([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], [100], 1)

  eight_checker = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
                   1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
                   999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
  test_one_output(eight_checker, [-100], 999)
  test_one_output(eight_checker, [7], 999)
  test_one_output(eight_checker, [8], 1000)
  test_one_output(eight_checker, [9], 1001)
  test_one_output(eight_checker, [100], 1001)

  pm("All tests pass.")

#test()

with open("input") as fin:
  line = fin.readline()
  original_program = [int(s) for s in line.split(",")]

p = Program(original_program)
p.set_input([5])
p.run_program()
print(p.get_output())

print("Final diagnostic code: {}".format(p.get_output()[-1]))