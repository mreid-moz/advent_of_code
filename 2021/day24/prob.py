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
      logging.debug(f"After applying [{i.line}], registers were {self.registers}")

big_computer = Computron()
computers = []
computer = None
for line in my_input:
  instr = Instruction(line)
  big_computer.add_instruction(instr)
  if instr.op == 'inp':
    if computer is not None:
      computers.append(computer)
    computer = Computron()
  computer.add_instruction(instr)
computers.append(computer)

logging.info(f"Found {len(computers)} computers")

dumb_computers = [None] * 14


def branch(digit, prev, subtract_amount, add_amount):
  m = prev % 26
  x = m + subtract_amount
  if x == digit:
    return prev // 26
  return prev - m + digit + add_amount

dumb_computers[0]  = lambda digit, prev: digit + 6
dumb_computers[1]  = lambda digit, prev: prev * 26 + digit + 7
dumb_computers[2]  = lambda digit, prev: prev * 26 + digit + 10
dumb_computers[3]  = lambda digit, prev: prev * 26 + digit + 2
dumb_computers[4]  = lambda digit, prev: branch(digit, prev, -7, 15)
dumb_computers[5]  = lambda digit, prev: prev * 26 + digit + 8
dumb_computers[6]  = lambda digit, prev: prev * 26 + digit + 1
dumb_computers[7]  = lambda digit, prev: branch(digit, prev, -5, 10)
dumb_computers[8]  = lambda digit, prev: prev * 26 + digit + 5
dumb_computers[9]  = lambda digit, prev: branch(digit, prev, -3, 3)
dumb_computers[10] = lambda digit, prev: branch(digit, prev,  0, 5)
dumb_computers[11] = lambda digit, prev: branch(digit, prev, -5, 11)
dumb_computers[12] = lambda digit, prev: branch(digit, prev, -9, 12)
dumb_computers[13] = lambda digit, prev: branch(digit, prev,  0, 10)

# Do some verifications:
#
# memo = [{},{},{},{},{},{},{},{},{},{},{},{},{},{}]
#
# for comp_idx in range(7):
#   for i in range(9):
#     digit = i + 1
#     previous_results = [0]
#     if comp_idx > 0:
#       previous_results = memo[comp_idx - 1].values()

#     for previous_result in previous_results:
#       computers[comp_idx].input = [digit]
#       computers[comp_idx].registers['z'] = previous_result
#       computers[comp_idx].run()

#       current_result = computers[comp_idx].registers['z']
#       dumb_result = dumb_computers[comp_idx](digit, previous_result)
#       if dumb_result != current_result:
#         logging.info(f"Mismatch with digit {digit} and prev {previous_result}: Dumb={dumb_result}, real={current_result}")
#         break
#       memo[comp_idx][(digit, previous_result)] = current_result
#       logging.debug(f"Running computer {comp_idx} with input {digit} and previous result {previous_result} produced result {current_result}")
#       #if comp_idx == 4 and (previous_result % 26) - 7 == digit:
#       #  logging.info(f"Previous result {previous_result} % 26 - 7 = {(previous_result % 26) - 7} == {digit}.")
#       computers[comp_idx].reset()
#   distinct_outputs = set(memo[comp_idx].values())
#   logging.info(f"Computer {comp_idx} produced {len(distinct_outputs)} distinct outputs. Min: {min(distinct_outputs)}, Max: {max(distinct_outputs)}")

# By default, count down from high nums
def check_all_combinations(computer, start=9, stop=0, step=-1):
  counter = 0
  for a in range(start, stop, step):
    a_result = dumb_computers[0](a, 0)
    for b in range(start, stop, step):
      b_result = dumb_computers[1](b, a_result)
      for c in range(start, stop, step):
        logging.info(f"Checking lists starting with {(a, b, c)}")
        c_result = dumb_computers[2](c, b_result)
        for d in range(start, stop, step):
          d_result = dumb_computers[3](d, c_result)
          for e in range(start, stop, step):
            e_result = dumb_computers[4](e, d_result)
            if e_result > d_result:
              continue
            for f in range(start, stop, step):
              f_result = dumb_computers[5](f, e_result)
              for g in range(start, stop, step):
                g_result = dumb_computers[6](g, f_result)
                for h in range(start, stop, step):
                  h_result = dumb_computers[7](h, g_result)
                  if h_result > g_result:
                    continue
                  for i in range(start, stop, step):
                    i_result = dumb_computers[8](i, h_result)
                    for j in range(start, stop, step):
                      j_result = dumb_computers[9](j, i_result)
                      if j_result > i_result:
                        continue
                      for k in range(start, stop, step):
                        k_result = dumb_computers[10](k, j_result)
                        if k_result > j_result:
                          continue
                        for l in range(start, stop, step):
                          l_result = dumb_computers[11](l, k_result)
                          if l_result > k_result:
                            continue
                          for m in range(start, stop, step):
                            m_result = dumb_computers[12](m, l_result)
                            if m_result > l_result:
                              continue
                            for n in range(start, stop, step):
                              final_result = dumb_computers[13](n, m_result)
                              if counter != 0 and counter % 5000000 == 0:
                                logging.info(f"{counter}th check had a result: {final_result} with inputs: {[a,b,c,d,e,f,g,h,i,j,k,l,m,n]}")
                              if final_result == 0:
                                return [a,b,c,d,e,f,g,h,i,j,k,l,m,n]
                              counter += 1

# answer = ''.join([str(i) for i in check_all_combinations(computer)])
# logging.info(f"Largest value: {answer}")

answer = ''.join([str(i) for i in check_all_combinations(computer, 1, 10, 1)])
logging.info(f"Small value: {answer}")


