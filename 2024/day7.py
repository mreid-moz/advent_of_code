from aocd.models import Puzzle
from collections import defaultdict
from itertools import product
import logging
import re
import sys

logging.basicConfig(level=logging.INFO)

p = Puzzle(year=2024, day=7)

TEST = False
if TEST:
    lines = p.examples[0].input_data.splitlines()
else:
    lines = p.input_data.splitlines()

def do_op(a, b, op):
    if op == '+':
        return a + b
    elif op == '*':
        return a * b
    elif op == '|':
        return int(f"{a}{b}")
    logging.error(f"Unexpected op: {op}")

def apply_ops(nums, ops):
    n = nums.copy()
    o = list(ops)
    result = n.pop(0)
    while len(n) > 0:
        b = n.pop(0)
        x = o.pop(0)
        r2 = do_op(result, b, x)
        result = r2
    return result

def get_valid_target(line, ops='+*'):
    target, remainder = line.split(": ")
    target = int(target)
    nums = [int(s) for s in remainder.split(' ')]

    for op_combo in product(ops, repeat=len(nums) - 1):
        result = apply_ops(nums, op_combo)
        # logging.debug(f"{target}: {remainder} with {op_combo} => {result}")
        if result == target:
            logging.info(f"Valid: {target}: {remainder} with {op_combo}")
            return target
    logging.debug(f"No op combo works for {target}: {remainder}")
    return None

# Part 1
valid_sum = 0
for line in lines:
    v = get_valid_target(line)
    if v is not None:
        valid_sum += v

logging.info(f"Found sum {valid_sum} of valid equations")

if not TEST:
    p.answer_a = valid_sum

# Part 2
valid_sum = 0
for line in lines:
    v = get_valid_target(line, ops='+*|')
    if v is not None:
        valid_sum += v

logging.info(f"Found sum {valid_sum} of valid equations including concat")

if not TEST:
    p.answer_b = valid_sum
