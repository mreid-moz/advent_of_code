from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.INFO)

p = Puzzle(year=2022, day=11)

lines = p.input_data.splitlines()
# lines = [
#   "Monkey 0:",
#   "  Starting items: 79, 98",
#   "  Operation: new = old * 19",
#   "  Test: divisible by 23",
#   "    If true: throw to monkey 2",
#   "    If false: throw to monkey 3",
#   "",
#   "Monkey 1:",
#   "  Starting items: 54, 65, 75, 74",
#   "  Operation: new = old + 6",
#   "  Test: divisible by 19",
#   "    If true: throw to monkey 2",
#   "    If false: throw to monkey 0",
#   "",
#   "Monkey 2:",
#   "  Starting items: 79, 60, 97",
#   "  Operation: new = old * old",
#   "  Test: divisible by 13",
#   "    If true: throw to monkey 1",
#   "    If false: throw to monkey 3",
#   "",
#   "Monkey 3:",
#   "  Starting items: 74",
#   "  Operation: new = old + 3",
#   "  Test: divisible by 17",
#   "    If true: throw to monkey 0",
#   "    If false: throw to monkey 1",
# ]

class Monkey:
  def __init__(self, name):
    self.name = name
    self.items = []
    self.operation = None
    self.operation_value = None
    self.test = None
    self.divisible_by = None
    self.true_monkey = None
    self.false_monkey = None
    self.business_count = 0

  def add(self, old):
    return old + self.operation_value
  def add_old(self, old):
    return old + old
  def mult(self, old):
    return old * self.operation_value
  def mult_old(self, old):
    return old * old

  def apply_operation(self, worry_level):
    new_worry_level = self.operation(worry_level)
    logging.debug(f"{self.name}: worry level went from {worry_level} to {new_worry_level}, then reduced to {new_worry_level // 3}")
    return new_worry_level // 3

  def parse_operation(self):
    logging.debug(f"Parsing operation {self.operation}")
    left, right = self.operation.split(' = ')
    if left != 'new':
      logging.warning(f"Unexpected LHS of operation {operation}: {left}")
      return
    s1, op, s2 = right.split(' ')
    if op == '+':
      if s2 == 'old':
        self.operation = self.add_old
      else:
        self.operation = self.add
        self.operation_value = int(s2)
    elif op == '*':
      if s2 == 'old':
        self.operation = self.mult_old
      else:
        self.operation = self.mult
        self.operation_value = int(s2)
    else:
      logging.warning(f"Unhandled operation: {op}")

  def inspect(self, item):
    self.business_count += 1
    new_item = self.apply_operation(item)
    if new_item % self.divisible_by == 0:
      logging.debug(f"{item} -> {new_item} is divisible by {self.divisible_by}, throwing to {self.true_monkey}")
      monkeys[self.true_monkey].items.append(new_item)
    else:
      logging.debug(f"{item} -> {new_item} NOT divisible by {self.divisible_by}, throwing to {self.false_monkey}")
      monkeys[self.false_monkey].items.append(new_item)

  def round(self):
    for item in self.items:
      self.inspect(item)
    self.items = []

monkeys = {}
monkey_list = []
current_monkey = None

for line in lines:
  if line.startswith("Monkey"):
    current_monkey = Monkey(line[:-1].lower()) # strip the ':', lowercase it.
    monkeys[current_monkey.name] = current_monkey
    monkey_list.append(current_monkey)
  elif line.startswith("  Starting items:"):
    current_monkey.items = [int(s) for s in line[18:].split(', ')]
  elif line.startswith("  Operation:"):
    current_monkey.operation = line[13:]
  elif line.startswith("  Test:"):
    current_monkey.test = line[8:]
    current_monkey.divisible_by = int(line[21:])
  elif line.startswith("    If true:"):
    current_monkey.true_monkey = line[22:]
  elif line.startswith("    If false:"):
    current_monkey.false_monkey = line[23:]
  elif line == '':
    continue
  else:
    logging.warning(f"Unexpected line: {line}")

for monkey in monkey_list:
  monkey.parse_operation()

for i in range(20):
  for monkey in monkey_list:
    monkey.round()
  logging.info(f"After {i+1} rounds:")
  for monkey in monkey_list:
    logging.info(f"  {monkey.name}: {monkey.items}")

top_monkey_business = 0
second_monkey_business = 0

for monkey in monkey_list:
  logging.debug(f"{monkey.name} inspected {monkey.business_count} times")
  if monkey.business_count > top_monkey_business:
    second_monkey_business = top_monkey_business
    top_monkey_business = monkey.business_count

logging.info(f"Monkey business: {top_monkey_business * second_monkey_business}")

p.answer_a = top_monkey_business * second_monkey_business
