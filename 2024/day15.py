from aocd.models import Puzzle
from collections import defaultdict
from utils import lines_to_map, draw_map
import logging
import re
import sys

logging.basicConfig(level=logging.INFO)

p = Puzzle(year=2024, day=15)

TEST = False
if TEST:
    lines = p.examples[0].input_data.splitlines()
    # lines = [
    #     "########",
    #     "#..O.O.#",
    #     "##@.O..#",
    #     "#...O..#",
    #     "#.#.O..#",
    #     "#...O..#",
    #     "#......#",
    #     "########",
    #     "",
    #     "<^^>>>vv<v>>v<<",
    # ]
else:
    lines = p.input_data.splitlines()

map_lines = []
move_lines = []
for line in lines:
    if line == '':
        logging.debug("Switching")
    elif line[0] == '#':
        map_lines.append(line)
    else:
        move_lines.append(line)

moves = "".join(move_lines)

def gps(x, y):
    return 100 * y + x

warehouse, min_x, max_x, min_y, max_y = lines_to_map(map_lines)
# draw_map(warehouse, max_x, max_y)

logging.info(f"Got Map size: {len(map_lines)}x{len(map_lines[0])}. Got {len(move_lines)} move lists.")

start = None
for (x, y), c in warehouse.items():
    if c == '@':
        start = (x, y)
        break
logging.info(f"Got Map size: {len(map_lines)}x{len(map_lines[0])}. Got {len(move_lines)} move lists. Start: {start}")

def get_range(x, dx, max_x):
    if dx < 0:
        return range(x-2, 0, dx)
    elif dx > 0:
        return range(x+2, max_x)

def move(m, loc, dx, dy, dc):
    sx, sy = loc
    nx, ny = (sx+dx, sy+dy)
    new_loc = (nx, ny)

    if new_loc not in m:
        logging.debug(f"We can move {dc} from {loc}")
        # move it directly
        del m[loc]
        m[new_loc] = '@'
        # return new_loc
    elif m[new_loc] == '#':
        logging.debug(f"can't move {dc} from {loc}")
        return loc
    elif m[new_loc] == 'O':
        moved = False
        if dx != 0:
            for x in get_range(sx, dx, max_x):
                if (x, sy) not in m:
                    logging.debug(f"We can move {dc} from {loc} (free spot at {x},{sy})")
                    m[(x, sy)] = 'O'
                    moved = True
                    break
                elif m[(x, sy)] == '#':
                    logging.debug(f"Can't shove {dc} from {loc} due to #")
                    break
        elif dy != 0:
            for y in get_range(sy, dy, max_y):
                if (sx, y) not in m:
                    logging.debug(f"We can move {dc} from {loc} (free spot at {sx},{y})")
                    m[(sx, y)] = 'O'
                    moved = True
                    break
                elif m[(sx, y)] == '#':
                    logging.debug(f"Can't shove {dc} from {loc} due to #")
                    break
        if moved:
            del m[loc]
            m[new_loc] = '@'
        else:
            logging.debug(f"can't move {dc} from {loc}, blocked by Os")
            return loc
    else:
        logging.error(f"can't move {dc} from {loc}, blocked by {m[new_loc]}")
        return loc

    return new_loc

move_it = {
    '<': lambda m, l, dc: move(m, l, -1,  0, dc),
    '>': lambda m, l, dc: move(m, l,  1,  0, dc),
    '^': lambda m, l, dc: move(m, l,  0, -1, dc),
    'v': lambda m, l, dc: move(m, l,  0,  1, dc),
}

logging.debug("Start:")
draw_map(warehouse, max_x, max_y, print_now=False,log=logging)

current = start
for c in moves:
    logging.debug(f"Moving {c} from {current}")
    current = move_it[c](warehouse, current, c)
    draw_map(warehouse, max_x, max_y, print_now=False,log=logging)
total_gps = 0
for (x, y), c in warehouse.items():
    if c == 'O':
        total_gps += gps(x, y)

logging.info(f"Total gps: {total_gps}")
if not TEST:
    p.answer_a = total_gps
