from aocd.models import Puzzle
from collections import defaultdict
from utils import lcm
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2023, day=8)

TEST = False
if TEST:
    lines = p.examples[0].input_data.splitlines()
else:
    lines = p.input_data.splitlines()

moves = lines[0]
num_moves = len(moves)

def get_move(i):
    return moves[i % num_moves]

path = {}

def get_steps(node, all_z=False):
    current = node
    steps = 0
    while True:
        if current == 'ZZZ':
            break
        if all_z is False and current[-1] == 'Z':
            break
        next_direction = get_move(steps)
        steps += 1
        current = path[current][next_direction]
    return steps

for line in lines[2:]:
    lhs, rhs = line.split(' = ')
    rl, rr = rhs[1:-1].split(', ')
    path[lhs] = {'L': rl, 'R': rr}

steps = get_steps('AAA', all_z=True)
logging.info("Took {} steps to get from AAA to ZZZ".format(steps))
if not TEST:
    p.answer_a = steps

# Part 2
currents = [k for k in path.keys() if k[-1] == 'A']
num_nodes = len(currents)
logging.info("Found {} nodes that end in A: {}".format(num_nodes, currents))
periods = [get_steps(c) for c in currents]
logging.info("Periods for each A node: {}".format(periods))

total_period = periods[0]
for period in periods[1:]:
    total_period = lcm(total_period, period)

logging.info("Total period: {}".format(total_period))

if not TEST:
    p.answer_b = total_period
