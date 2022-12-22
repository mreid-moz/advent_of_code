from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.INFO)

simple_pattern = re.compile(r"([a-z]+): ([\d]+)")
expr_pattern = re.compile(r"([a-z]+): ([a-z]+) ([-+*/]) ([a-z]+)")

p = Puzzle(year=2022, day=21)

TEST = False
# TEST = True

if TEST:
  lines = [
    "root: pppw + sjmn",
    "dbpl: 5",
    "cczh: sllz + lgvd",
    "zczc: 2",
    "ptdq: humn - dvpt",
    "dvpt: 3",
    "lfqf: 4",
    "humn: 5",
    "ljgn: 2",
    "sjmn: drzm * dbpl",
    "sllz: 4",
    "pppw: cczh / lfqf",
    "lgvd: ljgn * ptdq",
    "drzm: hmdt - zczc",
    "hmdt: 32",
  ]
else:
  lines = p.input_data.splitlines()

def apply(left, op, right):
  if op == '+':
    return left + right
  elif op == '-':
    return left - right
  elif op == '*':
    return left * right
  elif op == '/':
    return left // right

def inverse(left, op, right, target):
  if isinstance(left, int):
    # num op monkey = target
    if op == '+':
      # num + monkey = target
      return (right, target - left)
    elif op == '-':
      # num - monkey = target
      return (right, -1 * (target - left))
    elif op == '*':
      # num * monkey = target
      return (right, target // left)
    elif op == '/':
      # num / monkey = target
      return (right, left // target)
  elif isinstance(right, int):
    # monkey op num = target
    if op == '+':
      # monkey + num = target
      return (left, target - right)
    elif op == '-':
      # monkey - num = target
      return (left, target + right)
    elif op == '*':
      # monkey * num = target
      return (left, target // right)
    elif op == '/':
      # monkey / num = target
      return (left, target * right)
  else:
    logging.warning(f"Neither inverse was a number: L={left} O={op} R={right}, target={target}")

nums = {}
exps = {}
dependencies = {}

for line in lines:
  m = simple_pattern.match(line)
  if m:
    if m.group(1) == 'humn':
      logging.info(f"Found humn num: {line}")
      continue
    nums[m.group(1)] = int(m.group(2))
    logging.debug(f"Found a num: {m.group(1)} = {nums[m.group(1)]}")
    continue
  m = expr_pattern.match(line)
  if m:
    if m.group(1) == 'humn':
      logging.info(f"Found humn exp: {line}")
      continue
    exps[m.group(1)] = (m.group(2), m.group(3), m.group(4))
    logging.debug(f"Found an expression: {m.group(1)} = {m.group(2)} {m.group(3)} {m.group(4)}")

    for i in [2, 4]:
      if m.group(i) not in dependencies:
        dependencies[m.group(i)] = []
      dependencies[m.group(i)].append(m.group(1))
      logging.debug(f"Added dependency of {m.group(1)} to {m.group(i)}")
  else:
    logging.warning(f"Unexpected line: {line}")

logging.debug(f"Found {len(lines)} lines, of which {len(nums)} were nums and {len(exps)} were expressions.")

while len(nums) < len(lines):
  logging.info(f"We've solved {len(nums)} of {len(lines)}")
  exprs_to_remove = []
  nums_to_add = []
  num_updated = 0
  for monkey, val in nums.items():
    deps = dependencies.pop(monkey, [])
    if deps:
      logging.debug(f"Looking for dependencies for {monkey}: {deps}")
    for dep in deps:
      if dep in nums:
        continue
      if dep in exps:
        left, op, right = exps[dep]
        if left == monkey:
          logging.debug(f"Replacing left {monkey} with {val}")
          left = val
          num_updated += 1
        if right == monkey:
          right = val
          logging.debug(f"Replacing right {monkey} with {val}")
          num_updated += 1

        if isinstance(left, int) and isinstance(right, int):
          new_num = apply(left, op, right)
          nums_to_add.append((dep, new_num))
          logging.debug(f"Solved {dep}: {new_num}")
          exprs_to_remove.append(dep)
        else:
          exps[dep] = (left, op, right)
          logging.debug(f"Replacing expr for {dep} with {left} {op} {right}")
  for n, v in nums_to_add:
    nums[n] = v
  for e in exprs_to_remove:
    del exps[e]

  if num_updated == 0 and len(nums_to_add) == 0 and len(exprs_to_remove) == 0:
    logging.info("Didn't do anything, stopping :(")
    break

if 'root' in nums:
  logging.info(f"Root: {nums['root']}")
  # if not TEST:
  #   p.answer_a = nums['root']
elif 'root' in exps:
  logging.info(f"Root: {exps['root']}")
else:
  logging.warrning("Where the heck is 'root'?")

for monkey, (left, op, right) in exps.items():
  logging.info(f"Leftover expression: {monkey}: {left}{op}{right}")

root_left, root_op, root_right = exps['root']

next_target = None
next_monkey = None
if isinstance(root_left, int):
  next_target = root_left
  next_monkey = root_right
else:
  next_target = root_right
  next_monkey = root_left

logging.info(f"Need to make {next_monkey} == {next_target}")

while next_monkey != 'humn':
  left, op, right = exps[next_monkey]
  new_monkey, new_target = inverse(left, op, right, next_target)
  logging.info(f"Inverse of {next_monkey}: {left} {op} {right} -> {new_monkey}: {new_target}")
  next_monkey = new_monkey
  next_target = new_target

logging.info(f"Human should say {new_target}")

