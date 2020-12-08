import logging
import re
import sys

from computer import Computer, AbormalTermination
logging.basicConfig(level=logging.INFO)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [l.strip() for l in fin.readlines()]

comp = Computer(my_input)
last_accumulator = comp.accumulator

while True:
  instr = comp.get_current_instruction()
  last_accumulator = comp.accumulator
  if instr.visits > 0:
    break
  comp.step()

logging.info("Part 1: Accumulator value was {} before repeating".format(last_accumulator))

num_instructions = len(comp.instructions)
for i in range(num_instructions):
  logging.debug("Attempting to flip instruction {}".format(i))
  temp_comp = Computer(my_input)
  try_it = True
  if temp_comp.instructions[i].opcode == 'nop':
    logging.debug("s/nop/jmp/")
    temp_comp.instructions[i].opcode = 'jmp'
  elif temp_comp.instructions[i].opcode == 'jmp':
    logging.debug("s/jmp/nop/")
    temp_comp.instructions[i].opcode = 'nop'
  else:
    try_it = False

  if try_it:
    try:
      temp_comp.run()
      logging.info("Part 2: flipping instruction {} fixed it, accumulator value was {}".format(i, temp_comp.accumulator))
      break
    except:
      logging.debug("Flipping instruction {} didn't fix it.".format(i))
