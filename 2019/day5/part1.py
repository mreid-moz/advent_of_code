# --- Day 5: Sunny with a Chance of Asteroids ---
#
# You're starting to sweat as the ship makes its way toward Mercury. The Elves suggest that you get the air conditioner working by upgrading your ship computer to support the Thermal Environment Supervision Terminal.
#
# The Thermal Environment Supervision Terminal (TEST) starts by running a diagnostic program (your puzzle input). The TEST diagnostic program will run on your existing Intcode computer after a few modifications:
#
# First, you'll need to add two new instructions:
#
#     Opcode 3 takes a single integer as input and saves it to the position given by its only parameter. For example, the instruction 3,50 would take an input value and store it at address 50.
#     Opcode 4 outputs the value of its only parameter. For example, the instruction 4,50 would output the value at address 50.
#
# Programs that use these instructions will come with documentation that explains what should be connected to the input and output. The program 3,0,4,0,99 outputs whatever it gets as input, then halts.
#
# Second, you'll need to add support for parameter modes:
#
# Each parameter of an instruction is handled based on its parameter mode. Right now, your ship computer already understands parameter mode 0, position mode, which causes the parameter to be interpreted as a position - if the parameter is 50, its value is the value stored at address 50 in memory. Until now, all parameters have been in position mode.
#
# Now, your ship computer will also need to handle parameters in mode 1, immediate mode. In immediate mode, a parameter is interpreted as a value - if the parameter is 50, its value is simply 50.
#
# Parameter modes are stored in the same value as the instruction's opcode. The opcode is a two-digit number based only on the ones and tens digit of the value, that is, the opcode is the rightmost two digits of the first value in an instruction. Parameter modes are single digits, one per parameter, read right-to-left from the opcode: the first parameter's mode is in the hundreds digit, the second parameter's mode is in the thousands digit, the third parameter's mode is in the ten-thousands digit, and so on. Any missing modes are 0.
#
# For example, consider the program 1002,4,3,4,33.
#
# The first instruction, 1002,4,3,4, is a multiply instruction - the rightmost two digits of the first value, 02, indicate opcode 2, multiplication. Then, going right to left, the parameter modes are 0 (hundreds digit), 1 (thousands digit), and 0 (ten-thousands digit, not present and therefore zero):
#
# ABCDE
#  1002
#
# DE - two-digit opcode,      02 == opcode 2
#  C - mode of 1st parameter,  0 == position mode
#  B - mode of 2nd parameter,  1 == immediate mode
#  A - mode of 3rd parameter,  0 == position mode,
#                                   omitted due to being a leading zero
#
# This instruction multiplies its first two parameters. The first parameter, 4 in position mode, works like it did before - its value is the value stored at address 4 (33). The second parameter, 3 in immediate mode, simply has value 3. The result of this operation, 33 * 3 = 99, is written according to the third parameter, 4 in position mode, which also works like it did before - 99 is written to address 4.
#
# Parameters that an instruction writes to will never be in immediate mode.
#
# Finally, some notes:
#
#     It is important to remember that the instruction pointer should increase by the number of values in the instruction after the instruction finishes. Because of the new instructions, this amount is no longer always 4.
#     Integers can be negative: 1101,100,-1,4,0 is a valid program (find 100 + -1, store the result in position 4).
#
# The TEST diagnostic program will start by requesting from the user the ID of the system to test by running an input instruction - provide it 1, the ID for the ship's air conditioner unit.
#
# It will then perform a series of diagnostic tests confirming that various parts of the Intcode computer, like parameter modes, function correctly. For each test, it will run an output instruction indicating how far the result of the test was from the expected value, where 0 means the test was successful. Non-zero outputs mean that a function is not working correctly; check the instructions that were run before the output instruction to see which one failed.
#
# Finally, the program will output a diagnostic code and immediately halt. This final output isn't an error; an output followed immediately by a halt means the program finished. If all outputs were zero except the diagnostic code, the diagnostic program ran successfully.
#
# After providing 1 to the only input instruction and passing all the tests, what diagnostic code does the program produce?

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

    if opcode == 3:
      input_value = self.input.pop(0)
      self.program[pos1] = input_value
      self.offset += 2
      return True

    if opcode == 4:
      #pm("Outputting {} from offset {}".format(param1, self.offset))
      self.output.append(param1)
      self.offset += 2
      return True

    pos2 = self.program[self.offset + 2]
    pos3 = self.program[self.offset + 3]

    param2 = self.get_param(mode2, pos2)

    if opcode == 1:
      self.program[pos3] = param1 + param2
    elif opcode == 2:
      self.program[pos3] = param1 * param2
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

def test():
  test_one([1,0,0,0,99], [2,0,0,0,99])
  test_one([2,3,0,3,99], [2,3,0,6,99])
  test_one([2,4,4,5,99,0], [2,4,4,5,99,9801])
  test_one([1,1,1,4,99,5,6,0,99], [30,1,1,4,2,5,6,0,99])
  test_one([1002,4,3,4,33], [1002,4,3,4,99])
  test_one([1101,100,-1,4,0], [1101,100,-1,4,99])
  pm("All tests pass.")

#test()

with open("input") as fin:
  line = fin.readline()
  original_program = [int(s) for s in line.split(",")]

p = Program(original_program)
p.set_input([1])
p.run_program()
print(p.get_output())

print("Final diagnostic code: {}".format(p.get_output()[-1]))