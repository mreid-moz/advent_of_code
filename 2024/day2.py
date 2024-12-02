from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2024, day=2)

TEST = False
if TEST:
    lines = p.examples[0].input_data.splitlines()
else:
    lines = p.input_data.splitlines()

def is_safe(nums):
    diffs = []
    for i in range(len(nums)-1):
        if nums[i] == nums[i+1]:
            return False

        delta = nums[i] - nums[i+1]
        if abs(delta) > 3:
            return False
        diffs.append(delta)

    num_neg = len([x for x in diffs if x < 0])
    if num_neg != 0 and num_neg != len(diffs):
        return False
    return True

def is_safe_dampened(nums):
    # if is_safe(nums):
    #     return True
    for i in range(len(nums)):
        if i == 0:
            if is_safe(nums[1:]):
                return True
        else:
            if is_safe(nums[0:i] + nums[i+1:]):
                return True
    return False

num_safe = 0
num_damp_safe = 0
for line in lines:
    nums = [int(s) for s in line.split()]
    if is_safe(nums):
        num_safe += 1
        num_damp_safe += 1
    elif is_safe_dampened(nums):
        num_damp_safe += 1



if not TEST:
    p.answer_a = num_safe
    p.answer_b = num_damp_safe
