from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.INFO)

p = Puzzle(year=2024, day=4)

TEST = False
if TEST:
    lines = p.examples[0].input_data.splitlines()
else:
    lines = p.input_data.splitlines()

min_x = 0
min_y = 0
max_x = len(lines[0])
max_y = len(lines)

for line in lines:
    logging.debug(line)

def look(grid, x, y, xd, yd):
    if grid[y][x] != 'X':
        return False

    end_x  = x + 3 * xd
    if end_x < 0 or end_x >= len(grid[0]):
        return False
    end_y  = y + 3 * yd
    if end_y < 0 or end_y >= len(grid):
        return False
    if grid[y+yd][x+xd] != 'M':
        return False
    if grid[y+yd*2][x+xd*2] != 'A':
        return False
    if grid[y+yd*3][x+xd*3] != 'S':
        return False
    return True


def is_mas(a, b, c):
    mas = f"{a}{b}{c}"
    if mas == "MAS" or mas == "SAM":
        return True
    return False

def lookmas(grid, x, y):
    if grid[y][x] != 'A':
        return False

    if x < 1 or x >=  len(grid[0]) - 1:
        return False
    if y < 1 or y >= len(grid) - 1:
        return False

    if not is_mas(grid[y-1][x-1], grid[y][x], grid[y+1][x+1]):
        return False

    if not is_mas(grid[y-1][x+1], grid[y][x], grid[y+1][x-1]):
        return False
    return True

xmas_counter = 0
mas_counter = 0
for x in range(max_x):
    for y in range(max_y):
        if lookmas(lines, x, y):
            logging.info(f"MAS from {x}, {y}")
            mas_counter += 1

        if look(lines, x, y, -1, 0): # Look west
            logging.info(f"West from {x}, {y}")
            xmas_counter += 1
        if look(lines, x, y, 1, 0): # Look east
            logging.info(f"East from {x}, {y}")
            xmas_counter += 1
        if look(lines, x, y, 0, -1): # Look north
            logging.info(f"North from {x}, {y}")
            xmas_counter += 1
        if look(lines, x, y, 0, 1): # Look south
            logging.info(f"South from {x}, {y}")
            xmas_counter += 1
        if look(lines, x, y, -1, -1): # Look northwest
            logging.info(f"Northwest from {x}, {y}")
            xmas_counter += 1
        if look(lines, x, y, 1, -1): # Look northeast
            logging.info(f"Northeast from {x}, {y}")
            xmas_counter += 1
        if look(lines, x, y, -1, 1): # Look southwest
            logging.info(f"Southwest from {x}, {y}")
            xmas_counter += 1
        if look(lines, x, y, 1, 1): # Look southeast
            logging.info(f"Southeast from {x}, {y}")
            xmas_counter += 1

print(f"Found xmas {xmas_counter} times, mas {mas_counter} times")

if not TEST:
    p.answer_a = xmas_counter
    p.answer_b = mas_counter
