import logging
import re
import sys
from collections import defaultdict, deque

logging.basicConfig(level=logging.INFO)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [l.strip() for l in fin.readlines()]


class Instruction:
  def __init__(self, line):
    m = re.match('(inp|add|mul|div|mod|eql) ([wxyz]) ?([wxzy]|[0-9-]+)?', line)
    self.line = line
    if m:
      g = m.groups()
      self.op = g[0]
      self.register = g[1]
      self.arg = None
      if len(g) > 2:
        self.arg = g[2]
    else:
      logging.warning(f"Failed to parse instruction: {line}")


class Computron:
  def __init__(self):
    self.reset(True)

  def reset(self, include_instructions=False):
    self.registers = {
      'w': 0,
      'x': 0,
      'y': 0,
      'z': 0,
    }
    self.input = deque()
    if include_instructions:
      self.instructions = []

  def get_value(self, register_or_num):
    if re.match('[0-9-]', register_or_num):
      return int(register_or_num)
    return self.registers[register_or_num]

  def add_instruction(self, instruction):
    self.instructions.append(instruction)

  def run(self):
    for i in self.instructions:
      if i.op == 'inp':
        logging.debug(f"Before applying [{i.line}], registers were {self.registers}")
        self.registers['w'] = self.input.pop(0)
      elif i.op == 'add':
        self.registers[i.register] += self.get_value(i.arg)
      elif i.op == 'mul':
        self.registers[i.register] *= self.get_value(i.arg)
      elif i.op == 'div':
        self.registers[i.register] //= self.get_value(i.arg)
      elif i.op == 'mod':
        self.registers[i.register] %= self.get_value(i.arg)
      elif i.op == 'eql':
        if self.registers[i.register] == self.get_value(i.arg):
          self.registers[i.register] = 1
        else:
          self.registers[i.register] = 0
      #logging.debug(f"After applying [{i.line}], registers were {self.registers}")

computer = Computron()
for line in my_input:
  computer.add_instruction(Instruction(line))
# 9 -> 15
# 8 -> 14; 9 -> 380
# 7 -> 13; 9 -> 354
# 7 -> 13; 8 -> 354
# 2 -> 8
computer.input = [1,8,9,9,9,9,9,9,9,9,9,9,9,9]
#c.input = [9,9,9,9,9,9,9,9,9,9,9,9,9,9]
computer.run()
logging.info(f"Result: {computer.registers['z']}")

def check_all_combinations(computer):
  for a in range(9, 0, -1):
    for b in range(9, 0, -1):
      for c in range(9, 0, -1):
        for d in range(9, 0, -1):
          for e in range(9, 0, -1):
            for f in range(9, 0, -1):
              for g in range(9, 0, -1):
                for h in range(9, 0, -1):
                  for i in range(9, 0, -1):
                    for j in range(9, 0, -1):
                      logging.info(f"Checking lists starting with {(a, b, c, d, e, f, g, h, i, j)}")
                      for k in range(9, 0, -1):
                        for l in range(9, 0, -1):
                          for m in range(9, 0, -1):
                            for n in range(9, 0, -1):
                              computer.input = [a,b,c,d,e,f,g,h,i,j,k,l,m,n]
                              computer.run()
                              if computer.registers['z'] == 0:
                                return computer.input
                              computer.reset()

answer = ''.join([str(i) for i in check_all_combinations(computer)])
logging.info(f"Largest value: {answer}")