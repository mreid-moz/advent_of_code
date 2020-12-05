# --- Part Two ---
#
# "Good, the new computer seems to be working correctly! Keep it nearby during this mission - you'll probably use it again. Real Intcode computers support many more features than your new one, but we'll let you know what they are as you need them."
#
# "However, your current priority should be to complete your gravity assist around the Moon. For this mission to succeed, we should settle on some terminology for the parts you've already built."
#
# Intcode programs are given as a list of integers; these values are used as the initial state for the computer's memory. When you run an Intcode program, make sure to start by initializing memory to the program's values. A position in memory is called an address (for example, the first value in memory is at "address 0").
#
# Opcodes (like 1, 2, or 99) mark the beginning of an instruction. The values used immediately after an opcode, if any, are called the instruction's parameters. For example, in the instruction 1,2,3,4, 1 is the opcode; 2, 3, and 4 are the parameters. The instruction 99 contains only an opcode and has no parameters.
#
# The address of the current instruction is called the instruction pointer; it starts at 0. After an instruction finishes, the instruction pointer increases by the number of values in the instruction; until you add more instructions to the computer, this is always 4 (1 opcode + 3 parameters) for the add and multiply instructions. (The halt instruction would increase the instruction pointer by 1, but it halts the program instead.)
#
# "With terminology out of the way, we're ready to proceed. To complete the gravity assist, you need to determine what pair of inputs produces the output 19690720."
#
# The inputs should still be provided to the program by replacing the values at addresses 1 and 2, just like before. In this program, the value placed in address 1 is called the noun, and the value placed in address 2 is called the verb. Each of the two input values will be between 0 and 99, inclusive.
#
# Once the program has halted, its output is available at address 0, also just like before. Each time you try a pair of inputs, make sure you first reset the computer's memory to the values in the program (your puzzle input) - in other words, don't reuse memory from a previous attempt.
#
# Find the input noun and verb that cause the program to produce the output 19690720. What is 100 * noun + verb? (For example, if noun=12 and verb=2, the answer would be 1202.)


def step(program, offset):
  opcode = program[offset]
  if opcode == 99:
    return program, -1

  pos1 = program[offset + 1]
  pos2 = program[offset + 2]
  pos3 = program[offset + 3]

  if pos1 >= len(program):
    return program, -1
  if pos2 >= len(program):
    return program, -1
  if pos3 >= len(program):
    return program, -1

  if opcode == 1:
    program[pos3] = program[pos1] + program[pos2]
  elif opcode == 2:
    program[pos3] = program[pos1] * program[pos2]
  else:
    print("Unknown opcode: {}".format(opcode))
    return program, -1
  return program, offset + 4

def run_program(program):
  offset = 0
  while offset >= 0:
    program, offset = step(program, offset)
  return program

with open("input") as fin:
  line = fin.readline()
  original_program = [int(s) for s in line.split(",")]

print("1,0,0,0,99 -> {}".format(run_program([1,0,0,0,99])))
print("2,3,0,3,99 -> {}".format(run_program([2,3,0,3,99])))
print("2,4,4,5,99,0 -> {}".format(run_program([2,4,4,5,99,0])))
print("1,1,1,4,99,5,6,0,99 -> {}".format(run_program([1,1,1,4,99,5,6,0,99])))

updated_original = original_program.copy()

updated_original[1] = 12
updated_original[2] = 2
print("position 0 of original: {}".format(run_program(updated_original)[0]))

target_output = 19690720

def seek():
  for noun in range(100):
    for verb in range(100):
      fixed_program = original_program.copy()
      fixed_program[1] = noun
      fixed_program[2] = verb
      output = run_program(fixed_program)[0]
      if output == target_output:
  	    return (noun, verb, output)

noun, verb, output = seek()
print("Noun = {}, verb = {}, 100 * noun + verb = {}, output = {}".format(noun, verb, 100*noun+verb, output))