from aocd.models import Puzzle
from collections import defaultdict
from utils import draw_map, neighbours
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2024, day=12)

TEST = True
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

        "AAAAAA",
        "AAABBA",
        "AAABBA",
        "ABBAAA",  # => 368
        "ABBAAA",
        "AAAAAA",

        # "RRRRIICCFF",
        # "RRRRIICCCF",
        # "VVRRRCCFFF",
        # "VVRCCCJFFF",
        # "VVVVCJJCFE", # => 1206
        # "VVIVCCJJEE",
        # "VVIIICJJEE",
        # "MIIIIIJJEE",
        # "MIIISIJEEE",
        # "MMMISSJEEE",
    ]
else:
    lines = p.input_data.splitlines()

def flood(region_map, garden_map, x0, y0, x, y, max_x, max_y, level=0):
    logging.debug(f"Flood recursion level: {level}. originated at ({x0,y0}), currently looking at {x},{y}")

    if level > 8000:
        return

    if (x, y) not in region_map:
        n_area = 1
        n_perimeter = 4

        floods = []

        for nx, ny in neighbours(x, y, max_x, max_y, include_diagonals=False):
            logging.debug(f"Looking from {x},{y} to {nx},{ny}")
            if garden_map[(nx, ny)] == garden_map[(x, y)]:
                n_perimeter -= 1
                if (nx, ny) not in region_map:
                    floods.append((nx, ny))

        logging.debug(f"For {x},{y}, area={n_area}, per={n_perimeter}")
        if (x, y) == (x0, y0):
            region_map[(x, y)] = (n_area, n_perimeter)
        else:
            area, perimeter = region_map[(x0, y0)]
            area += n_area
            perimeter += n_perimeter
            region_map[(x, y)] = (-n_area, -n_perimeter)
            region_map[(x0, y0)] = (area, perimeter)

        for nx, ny in floods:
            flood(region_map, garden_map, x0, y0, nx, ny, max_x, max_y, level + 1)

def flood2(region_map, visited, garden_map, x0, y0, x, y, max_x, max_y, level=0):
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
            flood2(region_map, visited, garden_map, x0, y0, nx, ny, max_x, max_y, level + 1)


max_x = len(lines[0]) - 1
max_y = len(lines) - 1

garden_map = {}
for y in range(max_y+1):
    logging.debug(lines[y])
    for x in range(max_x+1):
        garden_map[(x, y)] = lines[y][x]

draw_map(garden_map, max_x, max_y)

regions = {}
for x in range(max_x+1):
    for y in range(max_y+1):
        if (x, y) in regions:
            continue
        logging.debug(f"Starting from ({x},{y})")
        flood(regions, garden_map, x, y, x, y, max_x, max_y, 0)

# draw_map(regions, max_x, max_y)

fence = 0
region_size = {}
for loc, size in regions.items():
    x, y = loc
    area, perimeter = size
    if area > 0:
        logging.debug(f"Region at {x},{y} has area {area}, perimeter {perimeter}")
        region_size[loc] = garden_map[loc]
        fence += area * perimeter
    else:
        region_size[loc] = str(-perimeter)

logging.info(f"Total fence: {fence}")
if not TEST:
    p.answer_a = fence

draw_map(region_size, max_x, max_y)

## Part 2
regions = defaultdict(set)
visited = set()
for x in range(max_x+1):
    for y in range(max_y+1):
        if (x, y) in visited:
            continue
        logging.debug(f"Starting from ({x},{y})")
        flood2(regions, visited, garden_map, x, y, x, y, max_x, max_y)

def check(target, x, y, m):
    return (x, y) in m and m[(x, y)] == target

def count_corners(x, y, m):

    #  | |
    # -+-+-
    #  |x|
    # -+-+-
    #  | |

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
    if not ne and not n and not e:
        # corner to the ne
        corners += 1
    if not se and not s and not e:
        # corner to the se
        corners += 1
    if not nw and not n and not w:
        # corner to the nw
        corners += 1
    if not sw and not s and not w:
        # corner to the sw
        corners += 1

    #  |x|
    # -+-+-
    #  |x|x
    # -+-+-
    #  | |
    # Count inside corners
    if not ne and n and e:
        # corner to the ne
        corners += 1
    if not se and s and e:
        # corner to the se
        corners += 1
    if not nw and n and w:
        # corner to the nw
        corners += 1
    if not sw and s and w:
        # corner to the sw
        corners += 1

    return corners


total_price = 0
for start, locations in regions.items():
    logging.debug(f"Region at {start} contained {locations}")
    sides = 0
    points_plus_exterior = set()

    for x, y in locations:
        for nx, ny in neighbours(x, y, max_x, max_y, min_x=-1, min_y=-1, include_diagonals=True):
            points_plus_exterior.add((nx, ny))
        n = count_corners(x, y, garden_map)
        logging.debug(f"{x},{y} had {n} corners")
        sides += n
    logging.info(f"Region {start} had {sides} sides")
    total_price += sides * len(locations)

logging.info(f"Total price: {total_price}")
if not TEST:
    p.answer_b = total_price


# EEEEE
# EXXXX
# EEEEE
# EXXXX
# EEEEE
