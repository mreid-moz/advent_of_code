from aocd.models import Puzzle
from collections import defaultdict
from utils import draw_map, neighbours
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2024, day=12)

TEST = False
if TEST:
    lines = p.examples[0].input_data.splitlines()
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


max_x = len(lines[0]) - 1
max_y = len(lines) - 1

garden_map = {}
regions = {}
for y in range(max_y+1):
    logging.debug(lines[y])
    for x in range(max_x+1):
        garden_map[(x, y)] = lines[y][x]

draw_map(garden_map, max_x, max_y)

for x in range(max_x+1):
    for y in range(max_y+1):
        if (x, y) in regions:
            continue
        logging.debug(f"Starting from ({x},{y})")
        flood(regions, garden_map, x, y, x, y, max_x, max_y, 0)

# draw_map(regions, max_x, max_y)

fence = 0
for loc, size in regions.items():
    x, y = loc
    area, perimeter = size
    if area > 0:
        logging.debug(f"Region at {x},{y} has area {area}, perimeter {perimeter}")
        fence += area * perimeter

logging.info(f"Total fence: {fence}")
if not TEST:
    p.answer_a = fence
