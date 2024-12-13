from aocd.models import Puzzle
from collections import defaultdict
from utils import draw_map, neighbours
import logging
import re
import sys

logging.basicConfig(level=logging.INFO)

p = Puzzle(year=2024, day=12)

TEST = False
if TEST:
    lines = p.examples[0].input_data.splitlines()
    lines = [
        # "OOOOO",
        # "OXOXO",
        # "OOOOO",
        # "OXOXO",
        # "OOOOO",

        # "EEEEE",
        # "EXXXX",
        # "EEEEE",
        # "EXXXX",
        # "EEEEE",

        # "AAAAAA",
        # "AAABBA",
        # "AAABBA",
        # "ABBAAA",  # => 368
        # "ABBAAA",
        # "AAAAAA",

        "RRRRIICCFF",
        "RRRRIICCCF",
        "VVRRRCCFFF",
        "VVRCCCJFFF",
        "VVVVCJJCFE", # => 1206
        "VVIVCCJJEE",
        "VVIIICJJEE",
        "MIIIIIJJEE",
        "MIIISIJEEE",
        "MMMISSJEEE",
    ]
else:
    lines = p.input_data.splitlines()

# identify all the separate regions using a flood-fill.
def flood(region_map, visited, garden_map, x0, y0, x, y, max_x, max_y, level=0):
    logging.debug(f"Flood2 recursion level: {level}. originated at ({x0,y0}), currently looking at {x},{y}")

    if (x, y) not in visited:
        visited.add((x, y))
        n_area = 1
        n_perimeter = 4

        floods = []

        for nx, ny in neighbours(x, y, max_x, max_y, include_diagonals=False):
            logging.debug(f"Looking from {x},{y} to {nx},{ny}")
            if garden_map[(nx, ny)] == garden_map[(x, y)]:
                if (nx, ny) not in region_map[(x0,y0)]:
                    floods.append((nx, ny))

        region_map[(x0, y0)].add((x, y))
        for nx, ny in floods:
            flood(region_map, visited, garden_map, x0, y0, nx, ny, max_x, max_y, level + 1)

def check(target, x, y, m):
    return (x, y) in m and m[(x, y)] == target

def count_corners(x, y, m):
    target = m[(x, y)]

    nw = check(target, x-1, y-1, m)
    ne = check(target, x+1, y-1, m)
    n = check(target, x, y-1, m)

    sw = check(target, x-1, y+1, m)
    se = check(target, x+1, y+1, m)
    s = check(target, x, y+1, m)

    e = check(target, x+1, y, m)
    w = check(target, x-1, y, m)

    corners = 0

    # Count outside corners
    if not n and not e: # corner to the ne
        corners += 1
    if not s and not e: # corner to the se
        corners += 1
    if not n and not w: # corner to the nw
        corners += 1
    if not s and not w: # corner to the sw
        corners += 1

    # Count inside corners
    if not ne and n and e: # corner to the ne
        corners += 1
    if not se and s and e: # corner to the se
        corners += 1
    if not nw and n and w: # corner to the nw
        corners += 1
    if not sw and s and w: # corner to the sw
        corners += 1

    return corners

max_x = len(lines[0]) - 1
max_y = len(lines) - 1

garden_map = {}
for y in range(max_y+1):
    logging.debug(lines[y])
    for x in range(max_x+1):
        garden_map[(x, y)] = lines[y][x]

regions = defaultdict(set)
visited = set()
for x in range(max_x+1):
    for y in range(max_y+1):
        if (x, y) in visited:
            continue
        logging.debug(f"Starting from ({x},{y})")
        flood(regions, visited, garden_map, x, y, x, y, max_x, max_y)

basic_price = 0 # part 1
discount_price = 0 # part 2
for start, locations in regions.items():
    logging.debug(f"Region at {start} contained {locations}")
    area = len(locations)
    sides = 0
    perimeter = 0
    for x, y in locations:
        # perimeter
        current_perimeter = 4
        for nx, ny in neighbours(x, y, max_x, max_y, include_diagonals=False):
            if garden_map[(nx, ny)] == garden_map[(x, y)]:
                current_perimeter -= 1
        perimeter += current_perimeter

        # sides (sides == cornes)
        corners = count_corners(x, y, garden_map)
        logging.debug(f"{x},{y} had {corners} corners")
        sides += corners

    logging.debug(f"Region {start} had perimeter {perimeter} and {sides} sides")
    basic_price += perimeter * area
    discount_price += sides * area

logging.info(f"Regular price: {basic_price}")
logging.info(f"Discount (sides) price: {discount_price}")
if not TEST:
    p.answer_a = basic_price
    p.answer_b = discount_price
