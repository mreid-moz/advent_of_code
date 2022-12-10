from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.INFO)

p = Puzzle(year=2022, day=10)

lines = p.input_data.splitlines()

class Add:
  def __init__(self, value):
    self.value = value
    self.cycles_needed = 2

  def apply(self, x):
    return x + self.value

  def __str__(self):
    return f"addx {self.value}"

class Noop:
  def __init__(self):
    self.cycles_needed = 1

  def apply(self, x):
    return x

  def __str__(self):
    return "noop"

class Dummy:
  def __init__(self):
    pass

  def apply(self, x):
    return x

  def __str__(self):
    return "dummy"

class Clock:
  def __init__(self):
    self.start_tick_x = 1
    self.x = 1
    self.cycle = 0
    self.instruction_queue = []

  def add_instruction(self, instr):
    for i in range(instr.cycles_needed - 1):
      self.instruction_queue.append(Dummy())
    self.instruction_queue.append(instr)

  def fast_forward(self, num_cycles):
    for i in range(num_cycles):
      self.tick()
    return self.x

  def signal_strength(self):
    return self.start_tick_x * self.cycle

  def tick(self):
    self.cycle += 1
    instr = self.instruction_queue.pop(0)
    self.start_tick_x = self.x
    self.x = instr.apply(self.x)
    logging.debug(f"Applying {instr}, x {self.start_tick_x} -> {self.x}")
    return self.x

def make_clock(lines):
  c = Clock()
  for line in lines:
    if line == 'noop':
      c.add_instruction(Noop())
    elif line.startswith('addx'):
      i, val = line.split(' ')
      c.add_instruction(Add(int(val)))
  return c

c = make_clock(lines)

signal_sum = 0

for i in [20, 40, 40, 40, 40, 40]:
  c.fast_forward(i)
  signal_sum += c.signal_strength()
  logging.debug(f"after {i} cycles, x was {c.x} ({c.start_tick_x}) and cycle counter was {c.cycle} for a signal strength of {c.signal_strength()}")

logging.info(f"Sum of signal strengths: {signal_sum}")
p.answer_a = signal_sum

# part b
c = make_clock(lines)
while c.instruction_queue:
  if abs((c.cycle % 40) - c.x) <= 1:
    print('#', end='')
  else:
    print(' ', end='')
  if c.cycle % 40 == 39:
    print('')
  c.tick()

