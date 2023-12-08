from aocd.models import Puzzle
from collections import defaultdict
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

for line in lines[2:]:
    lhs, rhs = line.split(' = ')
    rl, rr = rhs[1:-1].split(', ')
    path[lhs] = {'L': rl, 'R': rr}

current = 'AAA'
steps = 0
while current != 'ZZZ':
    next_direction = get_move(steps)
    steps += 1
    current = path[current][next_direction]

if not TEST:
    p.answer_a = steps

# Part 2
currents = [k for k in path.keys() if k[-1] == 'A']
num_nodes = len(currents)
logging.info("Found {} nodes that end in A: {}".format(num_nodes, currents))
num_zs = 0
steps = 0
while num_zs < num_nodes:
    next_direction = get_move(steps)
    steps += 1
    num_zs = 0
    for i in range(num_nodes):
        next_node = path[currents[i]][next_direction]
        currents[i] = next_node
        if next_node[-1] == 'Z':
            num_zs += 1
    if steps % 100 == 0:
        logging.debug("Step {}: {} Zs. {}".format(steps, num_zs, currents))

if not TEST:
    p.answer_b = steps