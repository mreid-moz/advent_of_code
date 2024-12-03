from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2024, day=3)

TEST = False
if TEST:
    lines = p.examples[0].input_data.splitlines()
    lines = ["xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"]
else:
    lines = p.input_data.splitlines()

pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")

def multiply(line):
    res = re.findall(pattern, line)
    total = 0
    for a, b in res:
        total += int(a) * int(b)
        # print(f"mul({a},{b})")
    return total

def multiply_conditional(line):
    # print(line)
    on = True
    total = 0
    for i in range(len(line)):
        if line[i:].startswith("don't()"):
            print(f"{i} turning off")
            on = False
        elif line[i:].startswith("do()"):
            print(f"{i} turning on")
            on = True
        else:
            m = re.match(pattern, line[i:])
            if m:
                a = int(m.group(1))
                b = int(m.group(2))
                print(f"{i} mul({a},{b}), on: {on}")
                if on:
                    total += a * b
                    # print(" and it was on")
                # else:
                #     print(" but it was off")
            # else:
            #     print(f"{i} found nothing")
    return total

total = sum([multiply(line) for line in lines])
# Don't reset the "on" state for each line, process it all in one string.
total_conditional = multiply_conditional(" ".join(lines))

print(f"total: {total}, conditional: {total_conditional}")
if not TEST:
    p.answer_a = total
    p.answer_b = total_conditional
