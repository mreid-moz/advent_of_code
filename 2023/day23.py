from aocd.models import Puzzle
from collections import defaultdict
from functools import cache
import logging
import re
import sys

sys.setrecursionlimit(50000)

logging.basicConfig(level=logging.INFO)

p = Puzzle(year=2023, day=23)

TEST = False
if TEST:
    lines = p.examples[0].input_data.splitlines()
else:
    lines = p.input_data.splitlines()

@cache
def longest(grid, visited, start, target, ignore_slopes=False):
    if start == target:
        return 0

    r, c = start
    visited = tuple([start] + list(visited))
    # visited.add(start)
    candidates = []
    for next_row, next_col, next_dir in [(r-1, c, '^'), (r+1, c, 'v'), (r, c-1, '<'), (r, c+1, '>')]:
        if next_row < 0 or next_row >= len(grid):
            continue
        if next_col < 0 or next_col >= len(grid[0]):
            continue

        if (next_row, next_col) in visited:
            logging.debug("Already visited {},{}".format(next_row, next_col))
            continue

        next_char = grid[next_row][next_col]
        if next_char == '#':
            continue

        if not ignore_slopes and (next_char != '.' and next_char != next_dir):
            logging.debug("Skipping {},{}, since it was {} and the slope was {}".format(next_row, next_col, next_dir, grid[next_row][next_col]))
            continue

        logging.debug("Searching from {},{} -> {},{} next".format(next_row, next_col, *target))
        candidate_length = longest(grid, visited, (next_row, next_col), target, ignore_slopes)
        if candidate_length is not None:
            candidates.append(candidate_length + 1)
            logging.debug("Longest from {},{} -> {},{} was {}".format(next_row, next_col, *target, candidates[-1]))
    if len(candidates) == 0:
        logging.debug("Found {} potential paths from {},{}".format(len(candidates), r, c))
        return None
    return max(candidates)

grid = tuple([tuple(line) for line in lines])

start_col = lines[0].find('.')
# distances, paths = dijkstra(lines, 0, start_col)
end_col = lines[-1].find('.')
# longest_dist = distances[(len(lines)-1, end_col)]

# Part A
longest_dist = longest(grid, tuple([]), (0, start_col), (len(grid)-1, end_col))
logging.info("Longest path from 0,{} to {},{}: {}".format(start_col, len(grid) - 1, end_col, longest_dist))

# draw_grid(grid, path)

if not TEST:
    p.answer_a = longest_dist

# Part B
longest_dist = longest(grid, tuple([]), (0, start_col), (len(grid)-1, end_col), ignore_slopes=True)
logging.info("Ignoring slopes, longest path from 0,{} to {},{}: {}".format(start_col, len(grid) - 1, end_col, longest_dist))


if not TEST:
    p.answer_b = longest_dist
