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
