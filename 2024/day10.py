from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.INFO)

p = Puzzle(year=2024, day=10)

TEST = False
if TEST:
    lines = p.examples[0].input_data.splitlines()
    lines = [
        "89010123",
        "78121874",
        "87430965",
        "96549874",
        "45678903",
        "32019012",
        "01329801",
        "10456732",
    ]
else:
    lines = p.input_data.splitlines()

def score(grid, xs, ys, rating=False):
    if grid[ys][xs] != '0':
        return 0

    potential_paths = [[(xs, ys)]]

    for i in range(1, 10):
        paths = list(potential_paths)
        potential_paths = []
        for path in paths:
            logging.debug(f"trying to extend path {path}")
            x, y = path[-1]
            logging.debug(f"from ({x},{y}), looking for {i}")
            for next_x, next_y in [(x,y-1), (x,y+1), (x-1,y), (x+1,y)]:
                if next_x < 0 or next_x >= len(grid[0]):
                    continue
                if next_y < 0 or next_y >= len(grid):
                    continue
                if int(grid[next_y][next_x]) == i:
                    logging.debug(f"Found a path: {path} + ({next_x},{next_y})")
                    potential_paths.append(path + [(next_x, next_y)])

    if rating:
        return len(potential_paths)
    nines = set()
    for p in potential_paths:
        nines.add(p[-1])

    return len(nines)

total_score = 0
for y in range(len(lines)):
    for x in range(len(lines[0])):
        total_score += score(lines, x, y)

logging.info(f"Sum of scores: {total_score}")

if not TEST:
    p.answer_a = total_score

total_rating = 0
for y in range(len(lines)):
    for x in range(len(lines[0])):
        total_rating += score(lines, x, y, rating=True)

logging.info(f"Sum of ratings: {total_rating}")

if not TEST:
    p.answer_b = total_rating
